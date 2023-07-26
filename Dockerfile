# Use a imagem base do FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho no contêiner
COPY requirements.txt .

# Atualize pip e instale as dependências especificadas no requirements.txt
RUN pip install -r requirements.txt

# Copie o restante dos arquivos do aplicativo para o diretório de trabalho

COPY . /app/