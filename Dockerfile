# # Use a imagem base do FastAPI
# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# # Defina o diretório de trabalho no contêiner
# WORKDIR /app

# # Copie o arquivo requirements.txt para o diretório de trabalho no contêiner
# COPY requirements.txt .

# # Atualize pip e instale as dependências especificadas no requirements.txt
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# # Copie o restante dos arquivos do aplicativo para o diretório de trabalho

# COPY . /app/

# CMD ["uvicorn", "fast_api.main:app", "--host", "0.0.0.0", "--port", "8080"]


# Use a imagem base do FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho no contêiner
COPY requirements.txt .

# Atualize pip e instale as dependências especificadas no requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos do aplicativo para o diretório de trabalho
COPY . /app/

# Utilize um script de inicialização para iniciar tanto o aplicativo FastAPI quanto o bot do Telegram
# Este script deve ser criado por você e adicionado ao seu projeto.
COPY start.sh /app/

# Torne o script de inicialização executável
RUN chmod +x /app/start.sh

# Execute o script de inicialização ao iniciar o contêiner
CMD ["/app/start.sh"]
