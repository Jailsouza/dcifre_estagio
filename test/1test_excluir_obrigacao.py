import pytest
from fastapi.testclient import TestClient


def test_excluir_obrigacao(client: TestClient, setup_db):

    """Testa a exclusão de uma obrigação acessória corretamente."""
    
    # Criar empresa primeiro
    empresa_data = {
        "nome": "Stark Industries",
        "cnpj": "11222333000144",
        "endereco": "Av. Tony Stark",
        "email": "contato@starkindustries.com",
        "telefone": "81997776655"
    }

    response = client.post("/empresas/", json=empresa_data)
    assert response.status_code == 200
    empresa = response.json()
    empresa_id = empresa["id"]

    # Criar obrigação acessória
    obrigacao_data = {
        "nome": "Declaração Mensal",
        "periodicidade": "MENSAL",
        "empresa_id": empresa_id
    }

    response = client.post("/obrigacoes_acessorias/", json=obrigacao_data)
    assert response.status_code == 200
    obrigacao = response.json()
    obrigacao_id = obrigacao["id"]

    # 🔹 Forçar o carregamento da empresa antes de excluir a obrigação
    response = client.get(f"/obrigacoes_acessorias/{obrigacao_id}/")
    assert response.status_code == 200
    obrigacao = response.json()

    # Excluir a obrigação acessória
    response = client.delete(f"/obrigacoes_acessorias/{obrigacao_id}/")
    assert response.status_code == 200  # Garante que a exclusão foi bem-sucedida

    # 🔹 Verificar se a obrigação foi removida corretamente
    response = client.get(f"/obrigacoes_acessorias/{obrigacao_id}/")
    assert response.status_code == 404  # Agora deve retornar um erro 404 (não encontrado)
