import pytest
from test_empresa import client, setup_db  # 🔹 Importando as fixtures de test_empresa.py

def test_criar_obrigacao(setup_db):  # 🔹 Removi `client` dos parâmetros
    empresa_data = {
        "nome": "Stark Industries",
        "cnpj": "11222333000144",
        "endereco": "Av. Tony Stark",
        "email": "contato@starkindustries.com",
        "telefone": "81997776655"
    }
    obrigacao_data = {
        "nome": "Declaração Mensal",
        "periodicidade": "mensal"
    }

    # Criando empresa e obrigacao
    response = client.post("/empresas/", json={**empresa_data, **obrigacao_data})
    empresa = response.json()
    obrigacao_id = empresa["obrigacoes_acessorias"][0]["id"]

    assert response.status_code == 200
    assert obrigacao_id is not None

def test_atualizar_obrigacao(setup_db):
    empresa_data = {
        "nome": "Stark Industries",
        "cnpj": "11222333000144",
        "endereco": "Av. Tony Stark",
        "email": "contato@starkindustries.com",
        "telefone": "81997776655"
    }
    obrigacao_data = {
        "nome": "Declaração Mensal",
        "periodicidade": "mensal"
    }

    response = client.post("/empresas/", json={**empresa_data, **obrigacao_data})
    empresa = response.json()
    obrigacao_id = empresa["obrigacoes_acessorias"][0]["id"]

    dados_atualizados = {
        "nome": "Declaração Anual",
        "periodicidade": "anual"
    }

    # Atualizando a obrigação
    response = client.put(f"/obrigacoes_acessorias/{obrigacao_id}", json=dados_atualizados)
    assert response.status_code == 200
    assert response.json()["nome"] == dados_atualizados["nome"]

def test_excluir_obrigacao(setup_db):
    empresa_data = {
        "nome": "Stark Industries",
        "cnpj": "11222333000144",
        "endereco": "Av. Tony Stark",
        "email": "contato@starkindustries.com",
        "telefone": "81997776655"
    }
    obrigacao_data = {
        "nome": "Declaração Mensal",
        "periodicidade": "mensal"
    }

    response = client.post("/empresas/", json={**empresa_data, **obrigacao_data})
    empresa = response.json()
    obrigacao_id = empresa["obrigacoes_acessorias"][0]["id"]

    # Excluindo a obrigação
    response = client.delete(f"/obrigacoes_acessorias/{obrigacao_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Obrigação acessória excluída com sucesso."}
