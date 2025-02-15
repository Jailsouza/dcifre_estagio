# Informativo sobre o Ambiente de Execução e Endpoints da API

## Ambiente Atual
O sistema está operando em modo: **🚀 Produção** ou **🧪 Teste** (conforme configurado no `.env`).

## Sobre o Projeto
Essa API foi desenvolvida como parte da **Prova de Seleção de Estágio**, utilizando **FastAPI, Pydantic e SQLAlchemy** para cadastro de empresas e gerenciamento de obrigações acessórias.

- **Nome completo**: Jailson Anegues de Souza
- **Site**: [jailson.dev.br](https://jailson.dev.br/)
- **Repositório GitHub**: [dcifre_estagio](https://github.com/Jailsouza/dcifre_estagio.git)

---

## 📜 **Documentação da API**
- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

---

## 🔹 **Endpoints Disponíveis**

### 📌 **Empresas**
- **Criar empresa**  
  `POST /empresas/`
  - Cadastro de uma nova empresa.
- **Listar empresas**  
  `GET /empresas/?skip={skip}&limit={limit}`
  - Retorna uma lista de empresas cadastradas.
- **Obter detalhes de uma empresa**  
  `GET /empresas/{empresa_id}/`
  - Retorna os detalhes de uma empresa específica.
- **Atualizar empresa**  
  `PUT /empresas/{empresa_id}/`
  - Atualiza os dados de uma empresa existente.
- **Excluir empresa**  
  `DELETE /empresas/{empresa_id}/`
  - Remove uma empresa do sistema.

---

### 📌 **Obrigações Acessórias**
- **Criar obrigação acessória**  
  `POST /obrigacoes_acessorias/`
  - Cadastra uma nova obrigação acessória.
- **Listar obrigações acessórias**  
  `GET /obrigacoes_acessorias/?skip={skip}&limit={limit}`
  - Retorna uma lista de obrigações acessórias cadastradas.
- **Atualizar obrigação acessória**  
  `PUT /obrigacoes_acessorias/{obrigacao_id}/`
  - Atualiza os dados de uma obrigação acessória existente.
- **Excluir obrigação acessória**  
  `DELETE /obrigacoes_acessorias/{obrigacao_id}/`
  - Remove uma obrigação acessória do sistema.

---

# Alterações realizadas no projeto

Apesar da recomendação do documento, realizei três alterações para facilitar o desenvolvimento do projeto:

### 1. Organização dos arquivos de teste  
Os arquivos de teste foram movidos para uma pasta específica para melhor organização. A pasta foi nomeada como **`test/`**.

### 2. Uso de `EmailStr` no modelo `Empresa`  
No modelo **`Empresa`** o campo `email` agora utiliza `EmailStr`, um tipo de dado fornecido pelo **Pydantic**, que valida automaticamente strings que devem conter endereços de e-mail válidos.

#### 📌 Estrutura original:
```sh
Empresa (Empresa): 
id: int (PK) 
nome: str 
cnpj: str (único) 
endereco: str 
email: str 
telefone: str
```

#### ✅ Estrutura atualizada:
```sh
Empresa (Empresa): 
id: int (PK) 
nome: str 
cnpj: str (único) 
endereco: str 
email: EmailStr 
telefone: str
```

### 3. Uso de `Enum` para o campo `periodicidade` no modelo `ObrigacaoAcessoria`  
Foi implementada a classe `PeriodicidadeEnum` para definir valores fixos para o campo `periodicidade`, garantindo maior consistência nos dados.

```python
from enum import Enum

class PeriodicidadeEnum(str, Enum):
    MENSAL = "MENSAL"
    TRIMESTRAL = "TRIMESTRAL"
    ANUAL = "ANUAL"
```

# Configuração do Ambiente

## Ambiente Virtual
```sh
python3 -m venv .venv
source .venv/bin/activate
```

## Instalação do PostgreSQL
```sh
brew install postgresql
```

## Iniciar e verificar o serviço do PostgreSQL
```sh
brew services list
brew services start postgresql
```

## Instalar Dependências
```sh
pip install "fastapi[all]" sqlalchemy psycopg2 pydantic python-dotenv
pip install psycopg2-binary pytest alembic pytest-cov
```

# Configuração do Banco de Dados

## Criar Bancos de Dados
```sql
CREATE DATABASE dbdcifre;
CREATE DATABASE dbdcifre_test;
```

## Criar Usuário e Configurar Acessos
```sql
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER USER postgres WITH SUPERUSER;
```

## Verificar e Excluir Banco Antes de Criar (Opcional)
```sql
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

CREATE DATABASE dbdcifre;
CREATE DATABASE dbdcifre_test;
```

# Migrações com Alembic

## Configurar Alembic
```sh
alembic init alembic
rm -rf alembic/
```

## Criar e Aplicar Migrações
```sh
alembic revision --autogenerate -m "Criar as tabelas"
alembic upgrade head
```

## Gerenciar Migrações
```sh
alembic history --verbose
alembic downgrade <revision_id>
alembic revision --autogenerate -m "Initial migration" --head <revision_id>
```

## Resetar Migrações
```sh
find alembic/ -mindepth 1 ! -name 'env.py' -exec rm -rf {} + && alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

# Testes

## Rodar o Pytest
```sh
pytest --maxfail=1 --disable-warnings -q
```

## Cobertura de Testes
```sh
pytest --cov=app
```

## Testar Modelos e Endpoints
```sh
# Testar os endpoints da Empresa (Empresa): 
python test/empresa/test_create_empresa_cnpj_duplicado.py
python test/empresa/test_create_empresa_cnpj_invalido.py
python test/empresa/test_delete_empresa.py
python test/empresa/test_empresa_operations.py.
python test/empresa/test_list_empresas.py
python test/empresa/test_update_empresa.py
# Testar os endpoints da Obrigação Acessória (ObrigacaoAcessoria):  
python test/obrigacao/test_create_obrigacao.py
python test/obrigacao/test_excluir_obrigacao.py
python test/obrigacao/test_listar_obrigacoes.py
python test/obrigacao/test_update_obrigacao.py
python test/test_main_routes.py
# listar os testes que o pytest encontrou no seu projeto sem realmente executá-los.
pytest --collect-only
```

# Executar a API
```sh
uvicorn main:app --reload
```

# Dependências e Documentação

## Gerar e Instalar Requirements
```sh
pip freeze > requirements.txt
pip install -r requirements.txt
```

## Documentação FastAPI
- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

## Links úteis
- [Pydantic - Live de Python #165](https://www.youtube.com/watch?v=UdfLu1G47BU)
- [pytest - Documentação](https://docs.pytest.org/en/stable/how-to/usage.html)
- [SQLAlchemy - Documentação](https://docs.sqlalchemy.org/en/20/index.html)

# Inserção de Dados (Exemplo)
```sql
INSERT INTO public.obrigacoes_acessorias(id, nome, periodicidade, empresa_id) VALUES
    (1, 'Declaração Mensal', 'MENSAL', 23),
    (2, 'Declaração Trimestral', 'TRIMESTRAL', 23),
    (3, 'Declaração Trimestral', 'TRIMESTRAL', 24),
    (4, 'Relatório de Impostos', 'MENSAL', 24),
    (5, 'Declaração de IRPJ', 'ANUAL', 25);
```

# Configurações Avançadas

## Adicionar Metadados ao Alembic
```python
from database import Base

target_metadata = Base.metadata  # A metadata que contém todas as tabelas
```