# test_models.py
from pydantic import ValidationError
from sqlalchemy.orm import Session
from schemas import EmpresaCreate, ObrigacaoAcessoriaCreate
from models import Empresa, ObrigacaoAcessoria
from database import SessionLocal  # Importando corretamente o SessionLocal de database.py


# Função para limpar o banco de dados (opcional, somente para ambiente de teste)
def reset_database():
    db: Session = SessionLocal()
    db.query(ObrigacaoAcessoria).delete()  # Deleta todas as obrigações acessórias
    db.query(Empresa).delete()  # Deleta todas as empresas
    db.commit()


# Lista de empresas fictícias para popular o banco de dados
empresas_vingadores = [
    {
        "nome": "Sigmeta S.A",
        "cnpj": "12345678000195",
        "endereco": "Rua Vitor José Fernandes, 318",
        "email": "jailson@jailson.dev.br",
        "telefone": "81988673977",
    },
    {
        "nome": "Stark Industries S.A.",
        "cnpj": "11222333000144",
        "endereco": "Av. Tony Stark, 1980",
        "email": "contato@starkindustries.com",
        "telefone": "81997776655"
    },
    {
        "nome": "Wakanda Tech Ltda.",
        "cnpj": "99888777000166",
        "endereco": "Rua Vibranium, 2020",
        "email": "suporte@wakandatech.com",
        "telefone": "81996665544"
    },
    {
        "nome": "Asgard Solutions",
        "cnpj": "55444333000122",
        "endereco": "Av. Odinson, 1500",
        "email": "atendimento@asgardsolutions.com",
        "telefone": "81995554433"
    },
    {
        "nome": "Pym Technologies",
        "cnpj": "66777888000199",
        "endereco": "Rua das Partículas, 300",
        "email": "contato@pymtech.com",
        "telefone": "81994443322"
    },
    {
        "nome": "Barton Agropecuária",
        "cnpj": "33444555000177",
        "endereco": "Fazenda Arqueira, 500",
        "email": "vendas@bartonagro.com",
        "telefone": "81993332211"
    },
    {
        "nome": "Romanoff Security",
        "cnpj": "22333444000188",
        "endereco": "Av. das Espiãs, 700",
        "email": "seguranca@romanoff.com",
        "telefone": "81992221100"
    }
]

# Função de teste para popular o banco com empresas
def testar_popular_empresas():
    try:
        # Resetando o banco de dados antes de rodar o teste
        reset_database()

        # Inserindo as empresas no banco de dados
        db: Session = SessionLocal()
        for empresa_data in empresas_vingadores:
            empresa = EmpresaCreate(**empresa_data)

            # Verificar se o CNPJ já existe
            empresa_existente = db.query(Empresa).filter(Empresa.cnpj == empresa.cnpj).first()

            if empresa_existente:
                print(f"A empresa com o CNPJ {empresa.cnpj} já existe no banco de dados.")
            else:
                nova_empresa = Empresa(**empresa.model_dump())  # Usando model_dump() em vez de dict()
                db.add(nova_empresa)
                db.commit()
                db.refresh(nova_empresa)
                print(f"Empresa salva no banco com ID: {nova_empresa.id}, Nome: {nova_empresa.nome}")

    except ValidationError as e:
        print("Erro de validação na empresa:", e)

# Função para testar a criação de uma obrigação acessória
def test_obrigacao_create():
    try:
        # Ensure the first company exists
        db: Session = SessionLocal()
        empresa_1 = db.query(Empresa).first()  # Get the first company from the database

        if not empresa_1:
            print("Nenhuma empresa encontrada. Adicionando a primeira empresa...")
            # If no company exists, create the first one
            empresa_1 = Empresa(**empresas_vingadores[0])  # Using the first company in the list
            db.add(empresa_1)
            db.commit()
            db.refresh(empresa_1)
            print(f"Empresa criada com ID: {empresa_1.id}, Nome: {empresa_1.nome}")
        
        # Create a valid obligation
        obrigacao = ObrigacaoAcessoriaCreate(
            nome="Declaração Mensal",
            periodicidade="mensal",
            empresa_id=empresa_1.id  # Use the ID of the first company
        )
        print("Obrigação criada com sucesso:", obrigacao)

        # Save the obligation in the database
        nova_obrigacao = ObrigacaoAcessoria(**obrigacao.model_dump())
        db.add(nova_obrigacao)
        db.commit()
        db.refresh(nova_obrigacao)
        print("Obrigação acessória salva no banco com ID:", nova_obrigacao.id)

        # Test with an invalid periodicity value
        try:
            obrigacao_invalida = ObrigacaoAcessoriaCreate(
                nome="Declaração Inválida",
                periodicidade="semanal",  # Invalid value
                empresa_id=empresa_1.id
            )
            db.add(ObrigacaoAcessoria(**obrigacao_invalida.model_dump()))  # Trying to save it
            db.commit()  # Expecting this to raise a validation error
        except ValidationError as e:
            print("Erro de validação na obrigação acessória:", e)

    except ValidationError as e:
        print("Erro de validação na obrigação acessória:", e)


# Função para listar todas as empresas no banco de dados
def listar_empresas():
    db: Session = SessionLocal()
    empresas = db.query(Empresa).all()  # Listar todas as empresas
    print("\nEmpresas no banco de dados:")
    for empresa in empresas:
        print(f"ID: {empresa.id}, Nome: {empresa.nome}, CNPJ: {empresa.cnpj}")

# Função para listar as obrigações acessórias associadas a uma empresa
def listar_obrigacoes_empresa(empresa_id: int):
    db: Session = SessionLocal()
    obrigacoes = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.empresa_id == empresa_id).all()  # Filtrando pelas obrigações da empresa
    print(f"\nObrigações acessórias da empresa com ID {empresa_id}:")
    for obrigacao in obrigacoes:
        print(f"ID: {obrigacao.id}, Nome: {obrigacao.nome}, Periodicidade: {obrigacao.periodicidade}")

# Executando os testes
if __name__ == "__main__":
    testar_popular_empresas()  # Popula o banco com empresas de teste
    test_obrigacao_create()  # Testa a criação de uma obrigação acessória
    listar_empresas()  # Listar todas as empresas no banco de dados
    listar_obrigacoes_empresa(1)  # Listar as obrigações associadas à empresa com ID 1
