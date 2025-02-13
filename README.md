# Prova de Seleção de Estágio - FastAPI, Pydantic e SQLAlchemy

Este repositório contém a implementação de uma API simples utilizando FastAPI, Pydantic e SQLAlchemy para cadastrar empresas e gerenciar obrigações acessórias que as empresas precisam declarar para o governo.

## Objetivo

O objetivo deste projeto é criar uma API que permita o cadastro de empresas e o gerenciamento de obrigações acessórias, utilizando as seguintes tecnologias:

- **FastAPI**: Para a criação da API.
- **Pydantic**: Para a validação de dados e criação de schemas.
- **SQLAlchemy**: Para a modelagem e interação com o banco de dados PostgreSQL.

## Requisitos da Prova

### 1. Configuração do Ambiente

a. Criar um repositório no GitHub e compartilhar o link (deixar link público).

b. **Para este projeto, colocar todos os arquivos na pasta raiz do repositório (sem criar subpastas).**

c. Criar um ambiente virtual e instalar as dependências necessárias:

```bash
pip install fastapi[all] sqlalchemy psycopg2 pydantic
