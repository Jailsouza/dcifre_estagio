# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": (
            "Prova de Seleção de Estágio\n"
            "Nome completo: JAILSON ANEGUES DE SOUZA\n"
            "Site: https://jailson.dev.br/\n"
            "Link: https://github.com/Jailsouza/dcifre_estagio.git"
        )
    }