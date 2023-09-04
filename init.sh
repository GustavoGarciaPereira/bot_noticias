#!/bin/bash

# Verifica se o arquivo .env já existe
if [ ! -f .env ]; then
    echo "Criando o arquivo .env..."
    echo "WEB_API_URL=http://web:8080" >> .env
    echo "TOKEN=''" >> .env
fi

# # Instala as dependências do Python (se necessário)
# echo "Instalando as dependências do Python..."
# pip install -r requirements.txt

# Faz o build das imagens Docker
echo "Fazendo o build das imagens Docker..."
sudo docker-compose build

# Inicia os contêineres com docker-compose
echo "Iniciando os contêineres com docker-compose..."
sudo docker-compose up -d

# Executa os testes com pytest
echo "Executando os testes com pytest..."
sudo docker-compose exec web pytest fast_api/test/test.py

# Desliga e remove os contêineres após a execução
echo "Desligando os contêineres com docker-compose..."
sudo docker-compose down
