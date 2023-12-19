#!/bin/bash

# Inicia o bot do Telegram em background
python /app/telegram/bot.py &

# Inicia o aplicativo FastAPI
uvicorn fast_api.main:app --host 0.0.0.0 --port 8080
