import sys
import os
from logging.config import fileConfig
from dotenv import load_dotenv  # Importando para carregar as variáveis de ambiente
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.declarative import declarative_base
from alembic import context

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Adicionar o caminho para os modelos (importar a Base de models.py)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))  # Ajuste conforme necessário

# Importando a Base para gerar a metadata
from models import Base  # Substitua pelo caminho correto do seu arquivo de modelos

# Alembic Configuração
config = context.config

# Interpretando o arquivo de configuração para o logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Definindo a metadata do seu modelo
target_metadata = Base.metadata  # A metadata que contém todas as tabelas

# Ajustando dinamicamente a URL de conexão com o banco de dados
# Usando variáveis de ambiente carregadas do .env
database_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME_PRODUCAO' if os.getenv('ENV') == 'prod' else 'DB_NAME_TESTE')}"
config.set_main_option('sqlalchemy.url', database_url)

print("[INFO]  env.py ", database_url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
