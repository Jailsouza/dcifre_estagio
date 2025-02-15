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

def test_criar_empresa_sem_obrigacao(setup_db):
    # Dados para criar a empresa
    empresa_data = {
        "nome": "Empresa Teste",
        "cnpj": "12345678000190",
        "endereco": "Rua Teste, 123",
        "telefone": "81123456789",
        "email": "contato@empresa.com",  # Incluindo o email
    }
    
    print("Enviando requisição para criar empresa...")
    response_empresa = client.post("/empresas/", json=empresa_data)
    print(f"Resposta da criação da empresa: {response_empresa.status_code} - {response_empresa.json()}")
    
    # Verifique se a resposta foi bem-sucedida
    assert response_empresa.status_code == 200  # Verifica que a empresa foi criada com sucesso
    empresa = response_empresa.json()

    # Verifique se a empresa tem um ID (significa que foi criada com sucesso)
    print(f"ID da empresa criada: {empresa['id']}")
    assert empresa["nome"] == empresa_data["nome"]
    assert empresa["cnpj"] == empresa_data["cnpj"]
    assert empresa["email"] == empresa_data["email"]


#####################

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