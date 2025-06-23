from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
from prometheus_flask_exporter import PrometheusMetrics
import os

app = Flask(__name__)

# Configuração do PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@postgres:5432/mydb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuração de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do Prometheus
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

# Modelo de Dados
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.title}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    logger.info('Acessando endpoint principal')
    return jsonify({"message": "Bem-vindo à API Flask com PostgreSQL e Monitoramento!"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    logger.info(f'Recuperadas {len(tasks)} tarefas')
    return jsonify([{"id": task.id, "title": task.title, "completed": task.completed} for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(title=data['title'], completed=data.get('completed', False))
    db.session.add(new_task)
    db.session.commit()
    logger.info(f'Tarefa criada: {new_task.title}')
    return jsonify({"id": new_task.id, "title": new_task.title}), 201

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "database": "connected"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)