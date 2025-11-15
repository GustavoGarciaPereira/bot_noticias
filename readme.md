# 📰 RSS News Bot - FastAPI & Telegram

Um sistema moderno de agregação de notícias com API RESTful em FastAPI e bot inteligente para Telegram, seguindo princípios de arquitetura em camadas e boas práticas de desenvolvimento.

## 🌟 Características

- **🚀 API FastAPI** - Documentação automática com Swagger/OpenAPI
- **🤖 Bot Telegram** - Interface conversacional intuitiva
- **🏗️ Arquitetura em Camadas** - Código organizado e maintainable
- **📊 Múltiplas Fontes** - Agregação de notícias do Google News RSS
- **🔍 Busca Avançada** - Filtros por categoria, data e termos
- **📈 Estatísticas** - Análises em tempo real
- **🐳 Containerização** - Deploy simplificado com Docker

## 🏗️ Arquitetura

```
rss-news-bot/
├── app/                          # FastAPI Application
│   ├── core/                     # Configurações e segurança
│   ├── models/                   # Modelos de dados
│   ├── schemas/                  # Schemas Pydantic
│   ├── repositories/             # Camada de acesso a dados
│   ├── services/                 # Lógica de negócio
│   ├── routers/                  # Endpoints da API
│   └── main.py                   # Aplicação principal
├── telegram-bot/                 # Bot do Telegram
│   ├── bot.py                    # Classe principal do bot
│   ├── config.py                 # Configurações
│   └── requirements.txt          # Dependências do bot
├── docker-compose.yml            # Orquestração de containers
├── requirements.txt              # Dependências da API
└── README.md                     # Documentação
```

## 📋 Pré-requisitos

- Python 3.9+
- Docker e Docker Compose (opcional)
- Conta no Telegram

## ⚙️ Configuração Rápida

### Método 1: Docker (Recomendado)

```bash
# Clone o repositório
git clone <seu-repositorio>
cd rss-news-bot

# Execute o script de inicialização
chmod +x init.sh
./init.sh
```

O script `init.sh` irá:
- ✅ Criar arquivo `.env` com variáveis de ambiente
- ✅ Instalar dependências Python
- ✅ Buildar imagens Docker
- ✅ Iniciar containers
- ✅ Executar testes automatizados

### Método 2: Desenvolvimento Local

```bash
# Configurar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
pip install -r telegram-bot/requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações
```

## 🔧 Configuração do Bot Telegram

1. **Criar Bot no Telegram:**
   ```bash
   # Busque por @BotFather no Telegram
   # Execute /newbot
   # Siga as instruções e guarde o token
   ```

2. **Configurar Variáveis de Ambiente:**
   ```env
   # .env
   TELEGRAM_BOT_TOKEN=seu_token_do_bot_aqui
   API_BASE_URL=http://localhost:8000
   ALLOWED_ORIGIN=http://localhost:3000
   RSS_FEED_URL=https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419
   ```

## 🚀 Execução

### Opção 1: Docker Compose
```bash
docker-compose up -d
```

### Opção 2: Execução Manual
```bash
# Terminal 1 - API FastAPI
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Bot Telegram
cd telegram-bot
python bot.py
```

## 📡 Acesso aos Serviços

- **🌐 API FastAPI:** http://localhost:8000
- **📚 Documentação Interativa:** http://localhost:8000/docs
- **📖 Documentação Alternativa:** http://localhost:8000/redoc

## 🤖 Comandos do Bot Telegram

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `/start` | Inicia o bot e mostra boas-vindas | `/start` |
| `/noticias` | 3 notícias rápidas | `/noticias` |
| `/digest` | Resumo diário (5 notícias) | `/digest` |
| `/digest N` | Resumo com N notícias | `/digest 10` |
| `/urgentes` | Notícias das últimas 2h | `/urgentes` |
| `/buscar TERMO` | Busca por termo | `/buscar tecnologia` |
| `/categorias` | Lista categorias disponíveis | `/categorias` |
| `/estatisticas` | Estatísticas do dia | `/estatisticas` |
| `/ajuda` | Mostra ajuda completa | `/ajuda` |

## 🛠️ API Endpoints Principais

### Notícias
- `GET /news/` - Lista todas as notícias
- `GET /news/search?q=termo` - Busca avançada
- `GET /news/categories` - Lista categorias
- `GET /news/sources` - Lista fontes
- `GET /news/today` - Notícias de hoje

### Telegram (Otimizado)
- `GET /telegram/digest?limit=5` - Resumo para bot
- `GET /telegram/search?q=termo` - Busca para bot
- `GET /telegram/breaking` - Notícias urgentes
- `GET /telegram/stats` - Estatísticas formatadas
- `GET /telegram/quick?limit=3` - Notícias rápidas

## 🧪 Testes

```bash
# Executar testes
docker-compose exec web pytest

# Executar testes com cobertura
docker-compose exec web pytest --cov=app

# Testes específicos
docker-compose exec web pytest tests/test_services.py -v
```

## 🔍 Exemplos de Uso

### Via API Directamente
```bash
# Notícias de tecnologia
curl "http://localhost:8000/telegram/search?q=tecnologia"

# Resumo diário
curl "http://localhost:8000/telegram/digest?limit=5"

# Estatísticas
curl "http://localhost:8000/telegram/stats"
```

### Via Bot Telegram
1. Busque seu bot no Telegram pelo username
2. Envie `/start` para iniciar
3. Use os comandos listados acima

## 🐛 Solução de Problemas

### Problemas Comuns

**Bot não responde:**
- Verifique se o token do bot está correto no `.env`
- Confirme que a API está rodando na porta 8000

**Erro de conexão com API:**
```bash
# Verifique se os serviços estão rodando
docker-compose ps

# Ver logs
docker-compose logs web
docker-compose logs bot
```

**Problemas de RSS:**
- Verifique a URL do feed no `.env`
- Confirme conexão com a internet

### Comandos Úteis
```bash
# Reiniciar serviços
docker-compose restart

# Ver logs em tempo real
docker-compose logs -f

# Parar todos os serviços
docker-compose down
```

## 📈 Monitoramento e Logs

```bash
# Logs da aplicação
docker-compose logs web

# Logs do bot
docker-compose logs bot

# Logs em tempo real
docker-compose logs -f web bot
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚠️ Aviso

Este projeto é para fins educacionais e de demonstração. Não é recomendado para uso em produção sem as devidas adaptações de segurança e monitoramento.

## 🆕 Atualizações da Versão 2.0

- ✅ Arquitetura em camadas (Repository/Service/Router)
- ✅ Bot Telegram com comandos avançados
- ✅ Sistema de busca e filtros
- ✅ Estatísticas em tempo real
- ✅ Containerização completa
- ✅ Documentação interativa
- ✅ Tratamento de erros robusto

---

**Desenvolvido com ❤️ usando FastAPI e Python-Telegram-Bot**

Para dúvidas e suporte, abra uma issue no repositório do projeto.