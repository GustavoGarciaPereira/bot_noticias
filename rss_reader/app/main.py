from fastapi import FastAPI
from app.core.security import add_cors_middleware
from app.routers import news, telegram

app = FastAPI(
    title="RSS Reader API",
    description="API para leitura de feeds RSS do Google News",
    version="1.0.0"
)

# Configura CORS
add_cors_middleware(app)

# Inclui routers
app.include_router(news.router)
app.include_router(telegram.router) 

# @app.get("/")
# def root():
#     """
#     Endpoint raiz
#     """
#     return {
#         "message": "RSS Reader API", 
#         "version": "1.0.0",
#         "docs": "/docs"
#     }

from fastapi import FastAPI
from app.core.security import add_cors_middleware
from app.routers import news, telegram  # Adicionar telegram

app = FastAPI(
    title="RSS Reader API",
    description="API para leitura de feeds RSS do Google News - Otimizada para Telegram",
    version="2.0.0"
)

# Configura CORS
add_cors_middleware(app)

# Inclui routers
app.include_router(news.router)
app.include_router(telegram.router)  # Novo router para Telegram

@app.get("/")
def root():
    return {
        "message": "RSS Reader API - Telegram Bot", 
        "version": "2.0.0",
        "endpoints": {
            "telegram": {
                "digest": "/telegram/digest?limit=5",
                "search": "/telegram/search?q=termo&limit=5",
                "category": "/telegram/category/{categoria}",
                "breaking": "/telegram/breaking",
                "stats": "/telegram/stats",
                "quick": "/telegram/quick?limit=3"
            },
            "news": {
                "all": "/news/",
                "search": "/news/search",
                "categories": "/news/categories",
                "sources": "/news/sources"
            }
        },
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}