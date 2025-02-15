import os
from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import (
    get_empresas, 
    get_empresa_by_id, 
    update_empresa, 
    delete_empresa, 
    get_obrigacoes, 
    update_obrigacao, 
    delete_obrigacao
)
import models
from schemas import (
    EmpresaCreate,
    EmpresaUpdate,
    ObrigacaoAcessoriaCreate,
    ObrigacaoAcessoriaUpdate,
    ObrigacaoAcessoriaResponse,
    Empresa
)

# Carregar as variáveis do .env
load_dotenv()

app = FastAPI(
    title="Prova de Seleção de Estágio - FastAPI, Pydantic e SQLAlchemy",
    description="""Criar uma API simples utilizando FastAPI, Pydantic, SQLAlchemy para cadastrar 
                empresas e gerenciar obrigações acessórias que a empresa precisa declarar para o 
                governo.""",
    version="1.0.0",
)


# Determinar o ambiente atual
ENV = os.getenv("ENV", "prod")  # Padrão: produção
AMBIENTE_ATUAL = "🚀 Produção" if ENV == "prod" else "🧪 TESTE"

@app.get("/")
def read_root():
    return {
        "message": (
            "Prova de Seleção de Estágio\n"
            "Nome completo: JAILSON ANEGUES DE SOUZA\n"
            "Site: [jailson.dev.br](https://jailson.dev.br/)\n"
            "Repositório: [GitHub](https://github.com/Jailsouza/dcifre_estagio.git)"
        ),
        "status": f"Sistema operando em modo: {AMBIENTE_ATUAL}",
        "endpoints": {
            "Documentação Swagger": "http://127.0.0.1:8000/docs",
            "Documentação ReDoc": "http://127.0.0.1:8000/redoc",
            
            "Empresas": {
                "Listar empresas": "GET http://127.0.0.1:8000/empresas/",
                "Criar empresa": "POST http://127.0.0.1:8000/empresas/",
                "Detalhar empresa": "GET http://127.0.0.1:8000/empresas/{empresa_id}/",
                "Atualizar empresa": "PUT http://127.0.0.1:8000/empresas/{empresa_id}/",
                "Excluir empresa": "DELETE http://127.0.0.1:8000/empresas/{empresa_id}/"
            },
            
            "Obrigações Acessórias": {
                "Listar obrigações": "GET http://127.0.0.1:8000/obrigacoes_acessorias/",
                "Criar obrigação": "POST http://127.0.0.1:8000/obrigacoes_acessorias/",
                "Atualizar obrigação": "PUT http://127.0.0.1:8000/obrigacoes_acessorias/{obrigacao_id}/",
                "Excluir obrigação": "DELETE http://127.0.0.1:8000/obrigacoes_acessorias/{obrigacao_id}/"
            }
        }

    }
# ============================
# Rotas para Empresas
# ============================

@app.post("/empresas/", response_model=Empresa)
def criar_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    empresa_existente = db.query(models.Empresa).filter(models.Empresa.cnpj == empresa.cnpj).first()
    if empresa_existente:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")

    db_empresa = models.Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=List[Empresa])
def listar_empresas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_empresas(db=db, skip=skip, limit=limit)

@app.get("/empresas/{empresa_id}/", response_model=Empresa)
def obter_detalhes_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = get_empresa_by_id(db, empresa_id)
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

@app.put("/empresas/{empresa_id}/", response_model=Empresa)
def atualizar_empresa(empresa_id: int, empresa: EmpresaUpdate, db: Session = Depends(get_db)):
    db_empresa = update_empresa(db, empresa_id, empresa)
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

@app.delete("/empresas/{empresa_id}/", response_model=Empresa)
def excluir_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = delete_empresa(db, empresa_id)
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

# ============================
# Rotas para Obrigações Acessórias
# ============================

@app.get("/obrigacoes_acessorias/", response_model=List[ObrigacaoAcessoriaResponse])
def listar_obrigacoes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_obrigacoes(db=db, skip=skip, limit=limit)

@app.post("/obrigacoes_acessorias/", response_model=ObrigacaoAcessoriaResponse)
def criar_nova_obrigacao(obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = db.query(models.ObrigacaoAcessoria).filter(
        models.ObrigacaoAcessoria.nome == obrigacao.nome, 
        models.ObrigacaoAcessoria.empresa_id == obrigacao.empresa_id
    ).first()
    
    if db_obrigacao:
        raise HTTPException(status_code=400, detail="Essa obrigação acessória já existe para essa empresa.")
    
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.model_dump())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.put("/obrigacoes_acessorias/{obrigacao_id}/", response_model=ObrigacaoAcessoriaResponse)
def atualizar_obrigacao(obrigacao_id: int, obrigacao: ObrigacaoAcessoriaUpdate, db: Session = Depends(get_db)):
    db_obrigacao = update_obrigacao(db, obrigacao_id, obrigacao)
    if not db_obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")
    return db_obrigacao

@app.delete("/obrigacoes_acessorias/{obrigacao_id}/", response_model=ObrigacaoAcessoriaResponse)
def excluir_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    return delete_obrigacao(db, obrigacao_id)
