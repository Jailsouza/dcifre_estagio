#!/bin/bash

# Criar diretórios para organização
mkdir -p test/empresa
mkdir -p test/obrigacao

# Renomear e mover arquivos relacionados à Empresa
mv test/test_criar_empresa_cnpj_duplicado.py test/empresa/test_create_empresa_cnpj_duplicado.py
mv test/test_criar_empresa_cnpj_invalido.py test/empresa/test_create_empresa_cnpj_invalido.py
mv test/test_listar_empresas.py test/empresa/test_list_empresas.py
mv test/test_empresa.py test/empresa/test_empresa_operations.py
mv test/test_atualizar_empresa.py test/empresa/test_update_empresa.py
mv test/test_excluir_empresa.py test/empresa/test_delete_empresa.py

# Renomear e mover arquivos relacionados à Obrigação Acessória
mv test/test_criar_obrigacao.py test/obrigacao/test_create_obrigacao.py
mv test/test_atualizar_obrigacao.py test/obrigacao/test_update_obrigacao.py
mv test/test_excluir_obrigacao.py test/obrigacao/test_delete_obrigacao.py
mv test/test_listar_obrigacoes.py test/obrigacao/test_list_obrigacoes.py

# Renomear e manter o teste geral no diretório principal
mv test/test_main.py test/test_main_routes.py

echo "Renomeação e organização concluídas com sucesso! ✅"
