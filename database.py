# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# Carregar o arquivo .env explicitamente
load_dotenv(dotenv_path=Path('.env'))

# Recuperar variáveis de ambiente com valores padrão para evitar erros
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
ENV = os.getenv("ENV", "dbdcifre_test")  # Assume "dbdcifre_test" por padrão

# Definir o nome do banco de dados corretamente
DB_NAME = os.getenv("DB_NAME_TESTE", "banco_teste") if ENV == "test" else os.getenv("DB_NAME_PRODUCAO", "dbdcifre")

# Criar a URL de conexão com o banco de dados de teste
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Imprimir os dados
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")
print(f"ENV: {ENV}")
print(f"DATABASE_URL: {DATABASE_URL}")

# Criar o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Criar a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir Base
Base = declarative_base()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
