import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from models import Empresa
from database import get_db

client = TestClient(app)

@pytest.fixture
def db():
    """Retorna uma sessão do banco de dados para testes."""
    session = next(get_db())  # Obtém uma sessão do banco
    yield session
    session.close()  # Fecha a sessão após o teste

@pytest.fixture
def empresa_existente(db: Session):
    """Cria e retorna uma empresa de teste no banco."""
    empresa = Empresa(
        nome="Empresa Teste",
        cnpj="12345678000195",
        endereco="Rua A, 100",
        email="teste@email.com",
        telefone="11987654321"
    )
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    return empresa

def test_excluir_empresa(db: Session, empresa_existente):
    """Testa se a empresa é excluída corretamente."""
    response = client.delete(f"/empresas/{empresa_existente.id}/")
    assert response.status_code == 200

    # Verifica se a empresa foi realmente deletada
    response = client.get(f"/empresas/{empresa_existente.id}/")
    assert response.status_code == 404
