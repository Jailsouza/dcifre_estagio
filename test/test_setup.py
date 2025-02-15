# test_setup.py
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import os
from dotenv import load_dotenv

# Carregar o arquivo .env explicitamente
load_dotenv(dotenv_path=Path('.env'))

# Recuperar variáveis de ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
ENV = os.getenv("ENV")
print(f"ENV: {ENV}")

# Verifica se o ambiente é de teste, se sim, usa o banco de teste
DB_NAME = os.getenv("DB_NAME_TESTE") if os.getenv("ENV") == "test" else os.getenv("DB_NAME_PRODUCAO")

# Cria a URL de conexão com o banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Imprimir os dados
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")
print(f"ENV: {ENV}")
print(f"DATABASE_URL: {DATABASE_URL}")

@pytest.fixture(scope="module")
def setup_db():
    # Criação do banco de dados de teste com a URL de conexão
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    yield db  # Disponibiliza a sessão de banco de dados para os testes

    db.rollback()  # Reverte qualquer alteração após os testes
    db.close()  # Fecha a sessão
    Base.metadata.drop_all(bind=engine)  # Remove as tabelas após os testes
