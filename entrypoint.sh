#!/bin/bash

# Espera o PostgreSQL
while ! nc -z postgres 5432; do
  echo "Aguardando PostgreSQL..."
  sleep 2
done

# Verifica as versões instaladas
echo "Versões instaladas:"
pip freeze | grep -E 'flask|sqlalchemy|gunicorn'

# Inicia a aplicação
exec gunicorn --bind 0.0.0.0:5000 main:app