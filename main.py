from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import criar_empresa, get_empresas
from schemas import EmpresaCreate, ObrigacaoAcessoriaCreate, Empresa

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API!"}

@app.post("/empresas/", response_model=Empresa)
def criar_nova_empresa(empresa: EmpresaCreate, obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    return criar_empresa(db=db, empresa=empresa, obrigacao=obrigacao)

@app.get("/empresas/", response_model=List[Empresa])
def listar_empresas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_empresas(db=db, skip=skip, limit=limit)

