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

# Teste para verificar erro ao criar empresa com CNPJ inválido
def test_criar_empresa_cnpj_invalido(client, setup_db):
    empresa_data = {
        "nome": "Empresa Teste",
        "cnpj": "1234567890",  # CNPJ inválido (menos de 14 dígitos)
        "endereco": "Rua Teste, 123",
        "email": "contato@empresa.com",
        "telefone": "81123456789"
    }
    response = client.post("/empresas/", json=empresa_data)
    print(response.status_code)
    assert response.status_code == 422  # Unprocessable Entity (validação do Pydantic falhou)