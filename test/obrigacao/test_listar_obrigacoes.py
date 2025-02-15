import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
from models import Empresa
from sqlalchemy.orm import Session

client = TestClient(app)

def test_listar_obrigacoes():
    response = client.get("/obrigacoes_acessorias/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
