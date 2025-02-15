import pytest

def test_excluir_obrigacao(client, setup_db):
    # Criar empresa primeiro
    empresa_data = {
        "nome": "Stark Industries",
        "cnpj": "11222333000144",
        "endereco": "Av. Tony Stark",
        "email": "contato@starkindustries.com",
        "telefone": "81997776655"
    }

    response = client.post("/empresas/", json=empresa_data)
    assert response.status_code == 200  # Garante que a empresa foi criada
    empresa = response.json()
    empresa_id = empresa["id"]

    # Criar obrigação acessória separadamente
    obrigacao_data = {
        "nome": "Declaração Mensal",
        "periodicidade": "MENSAL",
        "empresa_id": empresa_id  # 🔹 Associamos à empresa criada
    }

    response = client.post("/obrigacoes_acessorias/", json=obrigacao_data)
    assert response.status_code == 200  # Garante que a obrigação foi criada
    obrigacao = response.json()
    obrigacao_id = obrigacao["id"]

    # Excluir a obrigação acessória
    response = client.delete(f"/obrigacoes_acessorias/{obrigacao_id}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Obrigação acessória excluída com sucesso."}
