import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
from models import Empresa
from sqlalchemy.orm import Session

client = TestClient(app)

@pytest.fixture
def empresa_existente(db: Session):
    empresa = Empresa(nome="Empresa Teste", cnpj="12345678000195", endereco="Rua A, 100", email="teste@email.com", telefone="11987654321")
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    return empresa

def test_atualizar_empresa(empresa_existente):
    response = client.put(f"/empresas/{empresa_existente.id}/", json={"nome": "Empresa Atualizada"})
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Atualizada"
