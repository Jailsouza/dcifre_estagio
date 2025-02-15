from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base  # Importando corretamente o Base
from schemas import PeriodicidadeEnum

# Modelo de Empresa
class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da empresa")
    nome = Column(String(100), index=True, nullable=False, comment="Nome da empresa")
    cnpj = Column(String(14), unique=True, index=True, nullable=False, comment="CNPJ da empresa (14 dígitos, único)")
    endereco = Column(String(200), nullable=True, comment="Endereço completo da empresa")
    email = Column(String(100), unique=True, nullable=False, comment="E-mail de contato da empresa (único)")
    telefone = Column(String(11), nullable=True, comment="Telefone de contato da empresa (10 ou 11 dígitos)")

    # Relacionamento com o modelo ObrigacaoAcessoria
    obrigacoes_acessorias = relationship(
        "ObrigacaoAcessoria", back_populates="empresa", cascade="all, delete-orphan"
    )

# Modelo de Obrigação Acessória
class ObrigacaoAcessoria(Base):
    __tablename__ = "obrigacoes_acessorias"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da obrigação acessória")
    nome = Column(String(100), index=True, nullable=False, comment="Nome da obrigação acessória")
    periodicidade = Column(Enum(PeriodicidadeEnum), nullable=False, comment="Periodicidade da obrigação (mensal, trimestral, anual)")
    empresa_id = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False, comment="ID da empresa associada a esta obrigação")

    # Relacionamento com a empresa
    empresa = relationship("Empresa", back_populates="obrigacoes_acessorias")
