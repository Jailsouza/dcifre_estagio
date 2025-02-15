import pytest

def test_excluir_obrigacao(client, setup_db):  # 🔹 Adicione `client` como parâmetro
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

    # Excluindo a obrigação
    response = client.delete(f"/obrigacoes_acessorias/{obrigacao_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Obrigação acessória excluída com sucesso."}