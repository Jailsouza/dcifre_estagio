import pytest

def test_atualizar_obrigacao(client, setup_db):  # 🔹 Adicione `client` como parâmetro
    empresa_data = {
        "nome": "Stark Industries",
        "cnpj": "11222333000144",
        "endereco": "Av. Tony Stark",
        "email": "contato@starkindustries.com",
        "telefone": "81997776655"
    }
    obrigacao_data = {
        "nome": "Declaração Mensal",
        "periodicidade": "MENSAL"
    }

    response = client.post("/empresas/", json={**empresa_data, **obrigacao_data})
    empresa = response.json()
    obrigacao_id = empresa["obrigacoes_acessorias"][0]["id"]

    dados_atualizados = {
        "nome": "Declaração Anual",
        "periodicidade": "ANUAL"
    }

    # Atualizando a obrigação
    response = client.put(f"/obrigacoes_acessorias/{obrigacao_id}", json=dados_atualizados)
    assert response.status_code == 200
    assert response.json()["nome"] == dados_atualizados["nome"]
