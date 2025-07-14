#!/usr/bin/env python3
import logging
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from src.core.config import settings
from src.infrastructure.postgres_models import Base  # Importe seus modelos aqui

def init_database():
    """Inicializa o banco de dados com tabelas e dados iniciais"""
    try:
        # Cria engine sem pool para operações de inicialização
        engine = create_engine(
            f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres",
            isolation_level="AUTOCOMMIT"
        )
        
        # Verifica e cria o banco de dados se não existir
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'")
            )
            if not result.scalar():
                print(f"Criando banco de dados {settings.DB_NAME}...")
                conn.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
                print("Banco de dados criado com sucesso")
        
        # Agora conecta ao banco de dados específico
        app_engine = create_engine(
            f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
        
        # Cria todas as tabelas
        print("Criando tabelas...")
        Base.metadata.create_all(bind=app_engine)
        print("Tabelas criadas com sucesso")
        
        # Insere dados iniciais se necessário
        with app_engine.connect() as conn:
            # Exemplo: inserir categorias padrão
            check = conn.execute(text("SELECT COUNT(*) FROM lancamentos"))
            if check.scalar() == 0:
                print("Inserindo dados iniciais...")
                conn.execute(text("""
                    INSERT INTO lancamentos (valor, descricao, tipo, data) VALUES 
                    ('100', 'Recebimentos de vendas', 'CREDITO', '2025-01-01')
                """))
                print("Dados iniciais inseridos")
        
        return True
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {str(e)}")
        return False

if __name__ == "__main__":
    print("Iniciando inicialização do banco de dados...")
    if init_database():
        print("Banco de dados inicializado com sucesso")
    else:
        print("Falha na inicialização do banco de dados")
        exit(1)