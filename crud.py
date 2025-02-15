from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Empresa, ObrigacaoAcessoria
from schemas import EmpresaCreate, EmpresaUpdate, ObrigacaoAcessoriaCreate, ObrigacaoAcessoriaUpdate

# Criar Empresa
def criar_empresa(db: Session, empresa: EmpresaCreate):
    try:
        db_empresa = db.query(Empresa).filter(Empresa.cnpj == empresa.cnpj).first()
        if db_empresa:
            raise HTTPException(status_code=400, detail="CNPJ já cadastrado")

        db_empresa = Empresa(**empresa.model_dump())
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar empresa: {str(e)}")

# Listar Empresas
def get_empresas(db: Session, skip: int = 0, limit: int = 10):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Parâmetros 'skip' e 'limit' devem ser positivos")
    return db.query(Empresa).offset(skip).limit(limit).all()

# Buscar Empresa por ID
def get_empresa_by_id(db: Session, empresa_id: int):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return db_empresa

# Atualizar Empresa
def update_empresa(db: Session, empresa_id: int, empresa: EmpresaUpdate):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    update_data = empresa.model_dump(exclude_unset=True)  # 🔹 Ignora campos None
    for key, value in update_data.items():
        setattr(db_empresa, key, value)

    db.commit()
    db.refresh(db_empresa)
    return db_empresa

# Deletar Empresa (verificando se há obrigações associadas)
def delete_empresa(db: Session, empresa_id: int):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    # 🔹 Verifica se existem obrigações associadas antes de deletar
    if db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.empresa_id == empresa_id).first():
        raise HTTPException(status_code=400, detail="Não é possível excluir a empresa, pois há obrigações acessórias associadas")

    db.delete(db_empresa)
    db.commit()
    return db_empresa

# Criar Obrigação Acessória
def criar_obrigacao(db: Session, obrigacao: ObrigacaoAcessoriaCreate):
    try:
        # 🔹 Verifica se a empresa existe antes de criar a obrigação
        if not db.query(Empresa).filter(Empresa.id == obrigacao.empresa_id).first():
            raise HTTPException(status_code=400, detail="Empresa associada não encontrada")

        db_obrigacao = ObrigacaoAcessoria(**obrigacao.model_dump())
        db.add(db_obrigacao)
        db.commit()
        db.refresh(db_obrigacao)
        return db_obrigacao
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar obrigação acessória: {str(e)}")

# Listar Obrigações Acessórias
def get_obrigacoes(db: Session, skip: int = 0, limit: int = 10):
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="Parâmetros 'skip' e 'limit' devem ser positivos")
    return db.query(ObrigacaoAcessoria).offset(skip).limit(limit).all()

# Atualizar Obrigação Acessória
def update_obrigacao(db: Session, obrigacao_id: int, obrigacao: ObrigacaoAcessoriaUpdate):
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if not db_obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")

    update_data = obrigacao.model_dump(exclude_unset=True)  # 🔹 Ignora valores None
    for key, value in update_data.items():
        setattr(db_obrigacao, key, value)

    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

# Deletar Obrigação Acessória
def delete_obrigacao(db: Session, obrigacao_id: int):
    db_obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if not db_obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação acessória não encontrada")

    db.delete(db_obrigacao)
    db.commit()
    return db_obrigacao
