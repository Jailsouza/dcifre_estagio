# test_endpoints.py
import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import sessionmaker
from database import SessionLocal, Base
from models import Empresa, ObrigacaoAcessoria

# Configuração do cliente de teste
client = TestClient(app)

# Função para criar o banco de dados para os testes
@pytest.fixture(scope="module")
def setup_db():
    # Criar as tabelas no banco de dados real (garante que a tabela empresas seja criada)
    Base.metadata.create_all(bind=SessionLocal().bind)
    db = SessionLocal()
    try:
        # Reverter qualquer alteração após o teste
        yield db
    finally:
        # Limpeza após os testes (transação revertida ou apagamento dos dados)
        db.rollback()
        db.close()
        # Apenas depois dos testes, excluir as tabelas
        Base.metadata.drop_all(bind=SessionLocal().bind)

# Teste para listar empresas
def test_listar_empresas(client, setup_db):
    empresa_data = {
        "nome": "Wayne Enterprises",
        "cnpj": "22334455000166",
        "endereco": "Gotham City",
        "email": "contato@wayne.com",
        "telefone": "81998887766"
    }
    response_create = client.post("/empresas/", json=empresa_data)
    print(response_create.json())  # Adicione isso para depurar
    response = client.get("/empresas/")
    print(response.json())  # Adicione isso para depurar
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
