from typing import List, Optional, ForwardRef
from pydantic import BaseModel, field_validator, EmailStr, ConfigDict, model_validator
from enum import Enum
import re

# Enums
class PeriodicidadeEnum(str, Enum):
    MENSAL = "MENSAL"
    TRIMESTRAL = "TRIMESTRAL"
    ANUAL = "ANUAL"

# BaseModel para a empresa
class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str

    @field_validator('cnpj')
    def validar_cnpj(cls, v):
        cnpj_numerico = ''.join(filter(str.isdigit, v))
        if len(cnpj_numerico) != 14:
            raise ValueError('CNPJ deve ter exatamente 14 dígitos numéricos')
        return cnpj_numerico

    @field_validator('telefone')
    def validar_telefone(cls, v):
        numeros = re.sub(r'[^0-9]', '', v)
        if len(numeros) != 11:
            raise ValueError('Telefone deve ter exatamente 11 dígitos numéricos')
        return v

class EmpresaCreate(EmpresaBase):
    pass

# class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
#     id: int
#     model_config = ConfigDict(from_attributes=True)


# ForwardRef para evitar importação circular
ObrigacaoAcessoriaResponseRef = ForwardRef('ObrigacaoAcessoriaResponse')

class Empresa(EmpresaBase):
    id: int
    obrigacoes_acessorias: List[ObrigacaoAcessoriaResponseRef] = []  # ✅ Agora usa objetos, não IDs
    model_config = ConfigDict(from_attributes=True)

class EmpresaUpdate(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[str] = None
    endereco: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None

# BaseModel para obrigação acessória
class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: PeriodicidadeEnum
    empresa_id: int

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    pass

class ObrigacaoAcessoriaResponse(ObrigacaoAcessoriaBase):
    id: int
    empresa: Optional[EmpresaBase] = None  # ✅ Usa EmpresaBase para evitar referência circular
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

# Atualiza a referência para evitar problemas de importação circular
Empresa.model_rebuild()
ObrigacaoAcessoriaResponse.model_rebuild()
