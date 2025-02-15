#!/bin/bash

# Função para verificar erros e interromper o script em caso de falha
check_error() {
  if [ $? -ne 0 ]; then
    echo -e "\033[31m[ERRO]\033[0m Erro encontrado durante a execução do comando: $1"
    exit 1
  fi
}

# Função para exibir informações com formato
print_info() {
  echo -e "\033[34m[INFO]\033[0m $1"
}

# Função para exibir sucesso com formato
print_success() {
  echo -e "\033[32m[SUCESO]\033[0m $1"
}

# Função para exibir aviso com formato
print_warning() {
  echo -e "\033[33m[AVISO]\033[0m $1"
}

# Passo 1: Remover todas as variáveis definidas no .env
if [ -f .env ]; then
    print_info "Removendo variáveis do .env..."
    while IFS= read -r line; do
        # Ignora linhas vazias e comentários
        if [[ -n "$line" && ! "$line" =~ ^\s*# ]]; then
            # Extrai o nome da variável
            var_name=$(echo "$line" | cut -d '=' -f 1)
            print_info "Removendo variável: $var_name"
            unset "$var_name"
        fi
    done < .env
else
    print_warning "Arquivo .env não encontrado."
    exit 1
fi

# Passo 2: Recarregar o .env
print_info "Recarregando variáveis do .env..."
source .env

# Passo 3: Verificar se as variáveis foram recarregadas
print_info "Variáveis recarregadas:"
env | grep -E "$(paste -sd '|' <(grep -o '^[^=]*' .env))"

# Verificar se as variáveis de ambiente estão carregadas corretamente
print_info "Variáveis carregadas:"
echo -e "\033[35mDB_USER:\033[0m $DB_USER"
echo -e "\033[35mDB_PASSWORD:\033[0m $DB_PASSWORD"
echo -e "\033[35mDB_HOST:\033[0m $DB_HOST"
echo -e "\033[35mDB_PORT:\033[0m $DB_PORT"
echo -e "\033[35mDB_NAME_PRODUCAO:\033[0m $DB_NAME_PRODUCAO"
echo -e "\033[35mDB_NAME_TESTE:\033[0m $DB_NAME_TESTE"
echo -e "\033[35mENV:\033[0m $ENV"

# Definir o banco de dados correto com base no ambiente
if [ "$ENV" == "test" ]; then
  DB_NAME=$DB_NAME_TESTE
elif [ "$ENV" == "prod" ]; then
  DB_NAME=$DB_NAME_PRODUCAO
else
  print_warning "Ambiente não definido ou inválido. Usando banco de dados de produção por padrão."
  DB_NAME=$DB_NAME_PRODUCAO
fi

print_info "Usando banco de dados: $DB_NAME"

# 1. Conectar ao PostgreSQL e dropar os bancos de dados de produção e teste
print_info "Conectando ao PostgreSQL e droppando os bancos de dados..."

# Forçar desconexão das sessões ativas do banco de dados de produção
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME_PRODUCAO' AND pid <> pg_backend_pid();"
check_error "Desconectar sessões ativas no banco de dados $DB_NAME_PRODUCAO"

# Dropar o banco de dados de produção
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME_PRODUCAO;"
check_error "Dropar banco de dados $DB_NAME_PRODUCAO"

# Forçar desconexão das sessões ativas do banco de dados de teste
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME_TESTE' AND pid <> pg_backend_pid();"
check_error "Desconectar sessões ativas no banco de dados $DB_NAME_TESTE"

# Dropar o banco de dados de teste
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME_TESTE;"
check_error "Dropar banco de dados $DB_NAME_TESTE"

# 2. Recriar os bancos de dados de produção e teste
print_info "Recriando os bancos de dados..."
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d postgres -c "CREATE DATABASE $DB_NAME_PRODUCAO;"
check_error "Criar banco de dados $DB_NAME_PRODUCAO"
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d postgres -c "CREATE DATABASE $DB_NAME_TESTE;"
check_error "Criar banco de dados $DB_NAME_TESTE"

# 3. Mover o arquivo alembic/env.py para o mesmo nível do script .sh
print_info "Movendo o arquivo alembic/env.py para o mesmo nível do script .sh..."
mv alembic/env.py ./env.py
check_error "Movendo alembic/env.py para o nível correto"

# 4. Remover a pasta alembic/
print_info "Removendo a pasta alembic/..."
rm -rf alembic/
check_error "Remover a pasta alembic/"

# 5. Executar o comando alembic init alembic para recriar a estrutura do Alembic
print_info "Executando alembic init alembic para recriar a estrutura..."
alembic init alembic
check_error "Recriar estrutura do Alembic"

# 6. Mover o arquivo ./env.py de volta para alembic/env.py
print_info "Movendo o arquivo ./env.py de volta para alembic/env.py..."
mv ./env.py alembic/env.py
check_error "Mover ./env.py de volta para alembic/env.py"

# 7. Garantir que o Alembic está configurado corretamente para os modelos
print_info "Garantindo que os modelos estão configurados corretamente no Alembic..."

# Importar os modelos para garantir que o Alembic detecte a metadata
python -c "from models import Base; print(Base.metadata.tables)" 

# 8. Criar a primeira migração com alembic revision --autogenerate
print_info "Criando a primeira migração com alembic revision --autogenerate..."
alembic revision --autogenerate -m "Initial migration"
check_error "Criar migração inicial com Alembic"

# 9. Rodar a migração
print_info "Executando alembic upgrade head para aplicar as migrações..."
alembic upgrade head
check_error "Rodar migração Alembic"

# 10. Verificar se as tabelas foram criadas no banco de dados correto
print_info "Verificando se as tabelas foram criadas no banco de dados $DB_NAME..."
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME -c "\dt"
check_error "Verificar tabelas no banco de dados $DB_NAME"

# 11. Inserir dados nas tabelas de empresas e obrigações
print_info "Inserindo dados nas tabelas de empresas e obrigações..."

psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME -c "
INSERT INTO empresas (nome, cnpj, endereco, email, telefone) VALUES
('Empresa A', '12345678000190', 'Rua A, 100', 'empresaA@exemplo.com', '8112345678'),
('Empresa B', '23456789000101', 'Rua B, 200', 'empresaB@exemplo.com', '8112345678'),
('Empresa C', '34567890000112', 'Rua C, 300', 'empresaC@exemplo.com', '8132345678'),
('Empresa D', '45678901000123', 'Rua D, 400', 'empresaD@exemplo.com', '8142345678'),
('Empresa E', '56789012000134', 'Rua E, 500', 'empresaE@exemplo.com', '8152345678');
"
check_error "Inserir dados na tabela empresas"

# Inserir algumas obrigações para algumas empresas
psql -U $DB_USER -h $DB_HOST -p $DB_PORT -d $DB_NAME -c "
INSERT INTO obrigacoes_acessorias (nome, periodicidade, empresa_id) VALUES
('Declaração de Impostos', 'MENSAL', (SELECT id FROM empresas WHERE cnpj = '12345678000190')),
('Relatório de Contabilidade', 'TRIMESTRAL', (SELECT id FROM empresas WHERE cnpj = '12345678000190')),
('Declaração de Impostos', 'MENSAL', (SELECT id FROM empresas WHERE cnpj = '23456789000101')),
('Relatório Anual de Obrigações', 'ANUAL', (SELECT id FROM empresas WHERE cnpj = '23456789000101')),
('Declaração de Impostos', 'MENSAL', (SELECT id FROM empresas WHERE cnpj = '34567890000112')),
('Relatório de Contabilidade', 'TRIMESTRAL', (SELECT id FROM empresas WHERE cnpj = '34567890000112')),
('Declaração de Impostos', 'MENSAL', (SELECT id FROM empresas WHERE cnpj = '45678901000123'));
"
check_error "Inserir dados na tabela obrigacoes_acessorias"

print_success "Operação concluída com sucesso!"