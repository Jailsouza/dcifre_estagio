import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app  # Importe o aplicativo FastAPI
from dotenv import load_dotenv
from pathlib import Path
import os

from models import Empresa, ObrigacaoAcessoria

# Carregar o arquivo .env explicitamente
load_dotenv(dotenv_path=Path('.env'))

# Recuperar variáveis de ambiente com valores padrão para evitar erros
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
ENV = os.getenv("ENV", "test")  # Assume "test" por padrão

# Definir o nome do banco de dados corretamente
DB_NAME = os.getenv("DB_NAME_TESTE", "banco_teste") if ENV == "test" else os.getenv("DB_NAME_PRODUCAO", "banco_producao")

# Criar a URL de conexão com o banco de dados de teste
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criar o engine e a sessão do banco de dados
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Cria as tabelas antes dos testes e remove ao final."""
    print("🔹 Criando as tabelas no banco de dados de teste...")
    Base.metadata.drop_all(bind=engine)  # Limpa tabelas antes de criar
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")
    yield  # Aqui os testes são executados
    print("🔻 Removendo tabelas após os testes...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tabelas removidas com sucesso!")

@pytest.fixture
def db(setup_db):
    """Cria uma sessão do banco de dados de teste e limpa antes de cada teste."""
    session = TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)  # Limpa as tabelas
    Base.metadata.create_all(bind=engine)  # Recria as tabelas
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(db):
    """Cria um cliente de teste do FastAPI e sobrescreve `get_db`."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()






# import pytest
# from sqlalchemy.orm import Session
# from models import Empresa, ObrigacaoAcessoria
# from database import get_db

# @pytest.fixture
# def db():
#     """Retorna uma sessão do banco de dados para testes."""
#     session = next(get_db())
#     yield session
#     session.close()

@pytest.fixture
def empresa_existente(db: pytest.Session):
    """Cria uma empresa de teste para associar a obrigações acessórias."""
    empresa = Empresa(
        nome="Empresa Teste",
        cnpj="12345678000195",
        endereco="Rua A, 100",
        email="teste@email.com",
        telefone="11987654321"
    )
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    return empresa

@pytest.fixture
def obrigacao_existente(db: pytest.Session, empresa_existente):
    """Cria uma obrigação acessória associada a uma empresa de teste."""
    obrigacao = ObrigacaoAcessoria(
        nome="DCTF",
        periodicidade="MENSAL",
        empresa_id=empresa_existente.id
    )
    db.add(obrigacao)
    db.commit()
    db.refresh(obrigacao)
    return obrigacao
