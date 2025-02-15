## Ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

## Instalar o Postgresql
brew install postgresql

## Instalar dependencias
pip install "fastapi[all]" sqlalchemy psycopg2 pydantic python-dotenv

## Lista e startar o serviço do PgSQL
brew services list
brew services start postgresql

## Banco de dados
CREATE DATABASE dbdcifre;
CREATE DATABASE dbdcifre_test;

## Criar os acessos ao banco (Acesso fácil para fins didáticos)
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER USER postgres WITH SUPERUSER;

## Carregar as variáveis de ambiente do arquivo .env
pip install python-dotenv
touch .env

##
pip install psycopg2-binary 

## 
pip install pytest

## Rodar o pytest
pytest --maxfail=1 --disable-warnings -q

##
pip install alembic
alembic init alembic
rm -rf alembic/

## Criar as migrações / = makemigrations
alembic revision --autogenerate -m "Criar as tabelas"

## Rodar as migrações / = migrate
alembic upgrade head

##
<!-- 
-- Verifica se o banco de dados existe antes de excluí-lo
DO
$$
BEGIN
   IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'dbdcifre') THEN
      EXECUTE 'DROP DATABASE dbdcifre';
   END IF;
   
   IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'dbdcifre_test') THEN
      EXECUTE 'DROP DATABASE dbdcifre_test';
   END IF;
END
$$;

-- Criação dos bancos fora do bloco PL/pgSQL
-- Execute essas instruções em uma transação separada

CREATE DATABASE dbdcifre;
CREATE DATABASE dbdcifre_test; -->

find alembic/ -mindepth 1 ! -name 'env.py' -exec rm -rf {} + &&
alembic init alembic &&
alembic revision --autogenerate -m "Initial migration" &&
alembic upgrade head

##
rm -rf alembic/versions/*
DROP TABLE alembic_version;

##
alembic history --verbose
alembic downgrade <revision_id>
alembic revision --autogenerate -m "Initial migration" --head <revision_id>


## Testar o model populando ele e simulando um erro na "obrigação acessória" com  Periodicidade inválida 'semanal' 
python test_models.py 

## Carregar a aplicação
uvicorn main:app --reload

## Gerar requirements.txt
pip freeze > requirements.txt

## Rodar requirements
pip install -r requirements.txt

## Documentação FastAPI - Swagger UI
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc

## Pydantic - Live de Python #165
https://www.youtube.com/watch?v=UdfLu1G47BU
https://docs.pytest.org/en/stable/how-to/usage.html


## Inserir Obrigações manualmente 
INSERT INTO public.obrigacoes_acessorias(
    id, nome, periodicidade, empresa_id)
VALUES
    (1, 'Declaração Mensal', 'mensal', 23),
    (2, 'Declaração Trimestral', 'trimestral', 23),
    (3, 'Declaração Trimestral', 'trimestral', 24),
    (4, 'Relatório de Impostos', 'mensal', 24),
    (5, 'Declaração de IRPJ', 'trimestral', 25),
    (6, 'Declaração de CSLL', 'mensal', 25),
    (7, 'Relatório de Dividendos', 'anual', 26),
    (8, 'Declaração de Contribuições', 'mensal', 26),
    (9, 'Declaração de ICMS', 'mensal', 27),
    (10, 'Declaração de ISSQN', 'mensal', 27),
    (11, 'Relatório de Balanço', 'trimestral', 28),
    (12, 'Declaração de PIS', 'mensal', 28),
    (13, 'Relatório de Lucros', 'anual', 29),
    (14, 'Declaração de COFINS', 'mensal', 29),
    (15, 'Declaração de Contribuições Previdenciárias', 'mensal', 23),
    (16, 'Declaração de Imposto de Renda', 'anual', 23),
    (17, 'Relatório de Gastos Tributários', 'trimestral', 24),
    (18, 'Declaração de IPI', 'mensal', 24),
    (19, 'Declaração de Simples Nacional', 'mensal', 25),
    (20, 'Relatório de Ajustes Fiscais', 'trimestral', 25),
    (21, 'Declaração de Retenção de Impostos', 'mensal', 26),
    (22, 'Declaração de Impostos sobre a Renda', 'anual', 26),
    (23, 'Declaração Mensal', 'mensal', 27),
    (24, 'Declaração Trimestral', 'trimestral', 27);


## Cobertura de teste
pip install pytest-cov
pytest --cov=app

##
# Adicionar o caminho para os modelos (importar a Base de database.py)
from database import Base

# Obtenha a URL do banco de dados diretamente do alembic.ini
target_metadata = Base.metadata  # A metadata que contém todas as tabelas

##
pytest test/test_endpoints.py::test_listar_empresas 
pytest test/test_endpoints.py::test_criar_empresa_cnpj_duplicado 