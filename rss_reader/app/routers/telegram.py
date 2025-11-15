from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.routers.news import get_news_repository
from app.services.news_service import NewsService
from app.services.telegram_service import TelegramService
from app.repositories.news_repository import NewsRepository

router = APIRouter(prefix="/telegram", tags=["telegram"])

# Dependencies
def get_telegram_service(news_repository: NewsRepository = Depends(get_news_repository)):
    news_service = NewsService(news_repository)
    return TelegramService(news_service)

@router.get("/digest")
def get_daily_digest(
    limit: int = Query(5, description="Número de notícias no resumo"),
    telegram_service: TelegramService = Depends(get_telegram_service)
):
    """Resumo diário formatado para Telegram"""
    try:
        return telegram_service.get_daily_digest(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar resumo: {str(e)}")

@router.get("/search")
def search_news_telegram(
    q: str = Query(..., description="Termo de busca"),
    limit: int = Query(5, description="Número de resultados"),
    telegram_service: TelegramService = Depends(get_telegram_service)
):
    """Busca de notícias formatada para Telegram"""
    try:
        return telegram_service.search_news_for_telegram(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")

@router.get("/category/{category_name}")
def get_category_news_telegram(
    category_name: str,
    limit: int = Query(5, description="Número de notícias"),
    telegram_service: TelegramService = Depends(get_telegram_service)
):
    """Notícias por categoria formatadas para Telegram"""
    try:
        return telegram_service.get_news_by_category_telegram(category_name, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar categoria: {str(e)}")

@router.get("/breaking")
def get_breaking_news_telegram(
    limit: int = Query(3, description="Número de notícias urgentes"),
    telegram_service: TelegramService = Depends(get_telegram_service)
):
    """Notícias urgentes das últimas 2 horas"""
    try:
        return telegram_service.get_breaking_news(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notícias urgentes: {str(e)}")

@router.get("/stats")
def get_stats_telegram(telegram_service: TelegramService = Depends(get_telegram_service)):
    """Estatísticas formatadas para Telegram"""
    try:
        stats_text = telegram_service.get_news_stats_telegram()
        return {
            "text": stats_text,
            "parse_mode": "HTML"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar estatísticas: {str(e)}")

@router.get("/quick")
def get_quick_news(
    limit: int = Query(3, description="Número de notícias"),
    telegram_service: TelegramService = Depends(get_telegram_service)
):
    """Notícias rápidas em formato simples"""
    try:
        news_service = telegram_service.news_service
        news_items = news_service.get_all_news()[:limit]
        
        messages = []
        for item in news_items:
            # Formato mais simples e direto
            message = f"📰 {item.title}\n🔗 {item.link}"
            if item.source_name:
                message += f"\n🏢 {item.source_name}"
            
            messages.append({
                "text": message,
                "parse_mode": None,  # Texto simples
                "disable_web_page_preview": True
            })
        
        return {"messages": messages, "total": len(messages)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")