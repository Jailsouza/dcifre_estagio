import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database import Base, get_db
from main import app  # Importe o aplicativo FastAPI
from dotenv import load_dotenv
from pathlib import Path
import os

# Carregar o arquivo .env explicitamente
load_dotenv(dotenv_path=Path('.env'))

# Recuperar variáveis de ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
ENV = os.getenv("ENV")

# Verifica se o ambiente é de teste, se sim, usa o banco de teste
DB_NAME = os.getenv("DB_NAME_TESTE") if os.getenv("ENV") == "test" else os.getenv("DB_NAME_PRODUCAO")

# Cria a URL de conexão com o banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Imprimir os dados (opcional, para depuração)
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")
print(f"ENV: {ENV}")
print(f"DATABASE_URL: {DATABASE_URL}")

# Configuração do banco de dados de teste
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de dados de teste
try:
    Base.metadata.drop_all(bind=engine)  # Remove todas as tabelas existentes
    Base.metadata.create_all(bind=engine)  # Cria as tabelas
except Exception as e:
    print(f"Erro ao configurar o banco de dados: {e}")
    raise

@pytest.fixture
def db():
    """
    Fixture para criar uma sessão do banco de dados.
    A sessão é fechada automaticamente após o teste.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db):
    """
    Fixture para criar um cliente de teste (TestClient) do FastAPI.
    Substitui a dependência `get_db` para usar o banco de dados de teste.
    """
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    # Substitui a dependência `get_db` no aplicativo FastAPI
    app.dependency_overrides[get_db] = override_get_db

    # Retorna o TestClient configurado
    yield TestClient(app)

    # Limpa as substituições após o teste
    app.dependency_overrides.clear()

@pytest.fixture
def setup_db(db):
    """
    Fixture para limpar e recriar as tabelas do banco de dados antes de cada teste.
    """
    try:
        # Remove todas as tabelas
        Base.metadata.drop_all(bind=engine)
        # Cria as tabelas novamente
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Erro ao configurar o banco de dados: {e}")
        raise

    yield  # O teste é executado aqui

    try:
        # Limpa as tabelas novamente após o teste (opcional)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Erro ao limpar o banco de dados após o teste: {e}")
        raise