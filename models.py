from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base  # Importando o Base agora corretamente do arquivo database.py
from enum import Enum as PyEnum

# Definindo um Enum para periodicidade
class PeriodicidadeEnum(PyEnum):
    MENSAL = "mensal"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"

# Modelo de Empresa
class Empresa(Base):
    __tablename__ = 'empresas'

    # Definindo as colunas da tabela
    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da empresa")
    nome = Column(String(100), index=True, comment="Nome da empresa")  # Tamanho máximo de 100 caracteres
    cnpj = Column(String(14), unique=True, index=True, comment="CNPJ da empresa (14 dígitos, único)")  # Tamanho fixo de 14 dígitos
    endereco = Column(String(200), comment="Endereço completo da empresa")  # Tamanho máximo de 200 caracteres
    email = Column(String(100), unique=True, comment="E-mail de contato da empresa (único)")  # Tamanho máximo de 100 caracteres
    telefone = Column(String(11), comment="Telefone de contato da empresa (10 ou 11 dígitos)")  # Tamanho máximo de 11 dígitos

    # Relacionamento com o modelo ObrigacaoAcessoria
    obrigacoes_acessorias = relationship(
        "ObrigacaoAcessoria", back_populates="empresa", cascade="all, delete-orphan"
    )


# Modelo de Obrigação Acessória
class ObrigacaoAcessoria(Base):
    __tablename__ = 'obrigacoes_acessorias'

    # Definindo as colunas da tabela
    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da obrigação acessória")
    nome = Column(String(100), index=True, comment="Nome da obrigação acessória")  # Tamanho máximo de 100 caracteres
    periodicidade = Column(Enum(PeriodicidadeEnum), comment="Periodicidade da obrigação (mensal, trimestral, anual)")  # Usando Enum
    empresa_id = Column(Integer, ForeignKey('empresas.id'), comment="ID da empresa associada a esta obrigação")

    # Relacionamento com a empresa
    empresa = relationship("Empresa", back_populates="obrigacoes_acessorias")