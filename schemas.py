from typing import List
from pydantic import BaseModel, field_validator, EmailStr
import re

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str

    # Validador para CNPJ
    @field_validator('cnpj')
    def validar_cnpj(cls, v):
        if len(v) != 14 or not v.isdigit():
            raise ValueError('CNPJ deve ter 14 dígitos numéricos')
        return v

    # Validador para telefone
    @field_validator('telefone')
    def validar_telefone(cls, v):
        if not re.match(r'^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}$', v):
            raise ValueError('Telefone inválido. Insira um formato válido.')
        return v

# Usando a classe EmpresaCreate que herda de EmpresaBase
class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int
    obrigacoes: List['ObrigacaoAcessoria'] = []

    class Config:
        orm_mode = True

class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    empresa_id: int

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa_id: int

    class Config:
        orm_mode = True
