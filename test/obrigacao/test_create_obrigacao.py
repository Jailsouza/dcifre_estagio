import pytest
# from models import PeriodicidadeEnum  # Importe o enum
from schemas import PeriodicidadeEnum  # Importe o enum

def test_criar_obrigacao(client, setup_db):
    # Criar a empresa
    empresa_data = {
        "nome": "Stark Industries",
        "cnpj": "11222333000144",
        "endereco": "Av. Tony Stark",
        "email": "contato@starkindustries.com",
        "telefone": "81997776655"
    }
    response_empresa = client.post("/empresas/", json=empresa_data)
    assert response_empresa.status_code == 200
    empresa_id = response_empresa.json()["id"]

    # Criar a obrigação acessória
    obrigacao_data = {
        "nome": "Declaração Mensal",
        "periodicidade": PeriodicidadeEnum.MENSAL.value,  # Use o valor do enum
        "empresa_id": empresa_id
    }
    response_obrigacao = client.post("/obrigacoes_acessorias/", json=obrigacao_data)
    assert response_obrigacao.status_code == 200