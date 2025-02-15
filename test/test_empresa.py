import os
from pathlib import Path
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from main import app
from models import Base, Empresa
from database import get_db

# Carregar variáveis do arquivo .env
load_dotenv(dotenv_path=Path(".env"))

# Recuperar variáveis de ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
ENV = os.getenv("ENV")

# Verifica se o ambiente é de teste, se sim, usa o banco de teste
DB_NAME = os.getenv("DB_NAME_TESTE") if ENV == "test" else os.getenv("DB_NAME_PRODUCAO")

# Cria a URL de conexão com o banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"Usando DATABASE_URL: {DATABASE_URL}")

# Configuração do banco de dados de teste
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")  # Criando tabelas apenas uma vez por sessão de testes
def setup_test_db():
    Base.metadata.drop_all(bind=engine)  # Remove tabelas antigas para evitar conflitos
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)  # Remove tabelas após os testes

@pytest.fixture
def db(setup_test_db):  # Criamos um banco limpo antes de cada teste
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()

@pytest.fixture
def client(db: Session):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def setup_db(db: Session):
    db.query(Empresa).delete()
    db.commit()

def test_criar_empresa(client: TestClient, setup_db: None):
    empresa_data = {
        "nome": "Stark Industries",
        "cnpj": "11222333000144",
        "endereco": "Av. Tony Stark",
        "email": "contato@starkindustries.com",
        "telefone": "81997776655"
    }
    response = client.post("/empresas/", json=empresa_data)
    
    assert response.status_code == 200
    empresa_criada = response.json()
    assert "id" in empresa_criada
    assert empresa_criada["nome"] == empresa_data["nome"]

def test_listar_empresas(client: TestClient, setup_db: None):
    empresa_data = {
        "nome": "Wayne Enterprises",
        "cnpj": "22334455000166",
        "endereco": "Gotham City",
        "email": "contato@wayne.com",
        "telefone": "81998887766"
    }
    # Cria uma empresa
    client.post("/empresas/", json=empresa_data)

    # Lista as empresas
    response = client.get("/empresas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1