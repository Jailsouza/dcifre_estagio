from typing import List, Optional, ForwardRef
from pydantic import BaseModel, field_validator, EmailStr, ConfigDict, model_validator
from enum import Enum
import re

# Enums
class PeriodicidadeEnum(str, Enum):
    MENSAL = "mensal"
    TRIMESTRAL = "trimestral"
    ANUAL = "anual"

# BaseModel para a empresa
from pydantic import BaseModel, field_validator, ValidationError

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str

    @field_validator('cnpj')
    def validar_cnpj(cls, v):
        # Remove caracteres não numéricos (como traços e pontos)
        cnpj_numerico = ''.join(filter(str.isdigit, v))
        
        # Verifica se o CNPJ tem exatamente 14 dígitos
        if len(cnpj_numerico) != 14:
            raise ValueError('CNPJ deve ter exatamente 14 dígitos numéricos')
        
        return cnpj_numerico

    # Validador para telefone (apenas quantidade de caracteres)
    @field_validator('telefone')
    def validar_telefone(cls, v):
        numeros = re.sub(r'[^0-9]', '', v)  # Remove caracteres não numéricos
        if len(numeros) != 11:
            raise ValueError('Telefone deve ter exatamente 11 dígitos numéricos')
        return v

class EmpresaCreate(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str

# ForwardRef para evitar importação circular
ObrigacaoAcessoriaRef = ForwardRef('ObrigacaoAcessoria')

class Empresa(EmpresaBase):
    id: int
    obrigacoes_acessorias: List[ObrigacaoAcessoriaRef] = [] # type: ignore
    model_config = ConfigDict(from_attributes=True)

class EmpresaUpdate(EmpresaBase):
    pass

# BaseModel para obrigação acessória
class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: PeriodicidadeEnum
    empresa_id: int

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa: 'Empresa'  # Remova o Optional
    model_config = ConfigDict(from_attributes=True)

class ObrigacaoAcessoriaUpdate(BaseModel):
    nome: Optional[str] = None
    periodicidade: Optional[PeriodicidadeEnum] = None

    @model_validator(mode='after')
    def validar_campos(self):
        if not any([self.nome, self.periodicidade]):
            raise ValueError('Pelo menos um campo deve ser fornecido para atualização')
        return self

    model_config = ConfigDict(from_attributes=True)

# Atualize a referência
ObrigacaoAcessoria.model_rebuild()