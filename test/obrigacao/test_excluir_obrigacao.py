import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from models import ObrigacaoAcessoria
# from test.obrigacao.test_create_obrigacao import empresa_existente


@pytest.fixture
def obrigacao_existente(db: Session, empresa_existente):
    """Cria uma obrigação acessória associada a uma empresa de teste."""
    obrigacao = ObrigacaoAcessoria(
        nome="DCTF",
        periodicidade="MENSAL",
        empresa_id=empresa_existente.id
    )
    db.add(obrigacao)
    db.commit()
    db.refresh(obrigacao)
    return obrigacao

def test_excluir_obrigacao(db: Session, obrigacao_existente):
    """Testa se a obrigação acessória é excluída corretamente."""
    client = TestClient(app)  

    response = client.delete(f"/obrigacoes_acessorias/{obrigacao_existente.id}/")
    assert response.status_code == 200

    obrigacao_deletada = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_existente.id).first()
    assert obrigacao_deletada is None
