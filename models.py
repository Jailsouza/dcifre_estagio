from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da empresa")
    nome = Column(String, index=True, comment="Nome da empresa")
    cnpj = Column(String, unique=True, index=True, comment="CNPJ da empresa (único)")
    endereco = Column(String, comment="Endereço completo da empresa")
    email = Column(String, comment="E-mail de contato da empresa")
    telefone = Column(String, comment="Telefone de contato da empresa")

    obrigacoes = relationship("ObrigacaoAcessoria", back_populates="empresa")

class ObrigacaoAcessoria(Base):
    __tablename__ = 'obrigacoes_acessorias'

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da obrigação acessória")
    nome = Column(String, index=True, comment="Nome da obrigação acessória")
    periodicidade = Column(String, comment="Periodicidade da obrigação (mensal, trimestral, anual)")
    empresa_id = Column(Integer, ForeignKey('empresas.id'), comment="ID da empresa associada a esta obrigação")

    empresa = relationship("Empresa", back_populates="obrigacoes")
