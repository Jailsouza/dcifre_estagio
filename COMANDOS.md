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
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER USER postgres WITH SUPERUSER;


## Pydantic - Live de Python #165
https://www.youtube.com/watch?v=UdfLu1G47BU
