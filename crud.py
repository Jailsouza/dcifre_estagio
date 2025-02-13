from sqlalchemy.orm import Session
from models import Empresa, ObrigacaoAcessoria
from schemas import EmpresaCreate, ObrigacaoAcessoriaCreate

def criar_empresa(db: Session, empresa: EmpresaCreate, obrigacao: ObrigacaoAcessoriaCreate):
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)

    db_obrigacao = ObrigacaoAcessoria(**obrigacao.dict(), empresa_id=db_empresa.id)
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)

    return db_empresa, db_obrigacao

def get_empresas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Empresa).offset(skip).limit(limit).all()

def get_obrigacoes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ObrigacaoAcessoria).offset(skip).limit(limit).all()
