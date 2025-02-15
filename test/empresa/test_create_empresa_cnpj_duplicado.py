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
        
# Teste para verificar erro ao tentar criar uma empresa com CNPJ duplicado
def test_criar_empresa_cnpj_duplicado(client, setup_db):
    empresa_data_1 = {
        "nome": "Empresa A",
        "cnpj": "12345678000190",
        "endereco": "Rua 1, 123",
        "email": "empresa_a@teste.com",
        "telefone": "81423456782"
    }
    response_1 = client.post("/empresas/", json=empresa_data_1)
    assert response_1.status_code == 200  # Primeira empresa criada com sucesso

    # Tenta criar uma segunda empresa com o mesmo CNPJ
    empresa_data_2 = {
        "nome": "Empresa B",
        "cnpj": "12345678000190",  # Mesmo CNPJ
        "endereco": "Rua 2, 456",
        "email": "empresa_b@teste.com",
        "telefone": "81987654321"
    }
    response_2 = client.post("/empresas/", json=empresa_data_2)
    assert response_2.status_code == 400  # Erro de CNPJ duplicado
    assert response_2.json()["detail"] == "CNPJ já cadastrado"