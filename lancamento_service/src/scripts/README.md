# Inicializar banco de dados
docker-compose exec lancamentos python scripts/init_db.py

# Inicializar Elasticsearch
docker-compose exec consolidado python scripts/init_es.py
