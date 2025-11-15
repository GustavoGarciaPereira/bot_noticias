from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.services.news_service import NewsService
from app.repositories.news_repository import NewsRepository
from app.schemas.news import NewsSearchFilters

router = APIRouter(prefix="/news", tags=["news"])

# Dependencies
def get_news_repository():
    return NewsRepository()

def get_news_service(news_repository: NewsRepository = Depends(get_news_repository)):
    return NewsService(news_repository)

# Endpoints existentes...
@router.get("/", response_model=List[Dict[str, Any]])
def get_all_news(news_service: NewsService = Depends(get_news_service)):
    try:
        return news_service.get_news_with_formatted_response()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notícias: {str(e)}")

# NOVOS ENDPOINTS

@router.get("/search")
def search_news(
    q: Optional[str] = Query(None, description="Termo de busca"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    source: Optional[str] = Query(None, description="Filtrar por fonte"),
    days: Optional[int] = Query(7, description="Notícias dos últimos N dias"),
    news_service: NewsService = Depends(get_news_service)
):
    """Busca notícias com múltiplos filtros"""
    try:
        date_from = datetime.now() - timedelta(days=days) if days else None
        
        filters = NewsSearchFilters(
            search_term=q,
            category=category,
            source=source,
            date_from=date_from
        )
        
        results = news_service.search_news(filters)
        return [
            {
                "title": item.title,
                "link": item.link,
                "pub_date": item.pub_date,
                "source_name": item.source_name,
                "categories": item.categories,
                "has_image": bool(item.media_content or item.media_thumbnail)
            }
            for item in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")

@router.get("/categories")
def get_categories(news_service: NewsService = Depends(get_news_service)):
    """Retorna todas as categorias disponíveis"""
    try:
        return news_service.get_news_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar categorias: {str(e)}")

@router.get("/sources")
def get_sources(news_service: NewsService = Depends(get_news_service)):
    """Retorna todas as fontes disponíveis"""
    try:
        return news_service.get_news_sources()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar fontes: {str(e)}")

@router.get("/category/{category_name}")
def get_news_by_category(
    category_name: str,
    news_service: NewsService = Depends(get_news_service)
):
    """Retorna notícias por categoria específica"""
    try:
        news_items = news_service.get_news_by_category(category_name)
        return [
            {
                "title": item.title,
                "link": item.link,
                "pub_date": item.pub_date,
                "source_name": item.source_name
            }
            for item in news_items
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar por categoria: {str(e)}")

@router.get("/today")
def get_todays_news(news_service: NewsService = Depends(get_news_service)):
    """Retorna notícias de hoje"""
    try:
        news_items = news_service.get_todays_news()
        return [
            {
                "title": item.title,
                "link": item.link,
                "source_name": item.source_name,
                "pub_date": item.pub_date
            }
            for item in news_items
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notícias de hoje: {str(e)}")

@router.get("/with-images")
def get_news_with_images(news_service: NewsService = Depends(get_news_service)):
    """Retorna notícias que possuem imagens"""
    try:
        news_items = news_service.get_news_with_images()
        return [
            {
                "title": item.title,
                "link": item.link,
                "source_name": item.source_name,
                "media_thumbnail": item.media_thumbnail,
                "media_content": item.media_content
            }
            for item in news_items
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notícias com imagens: {str(e)}")

@router.get("/stats/sources")
def get_news_stats_by_source(news_service: NewsService = Depends(get_news_service)):
    """Retorna estatísticas de notícias por fonte"""
    try:
        return news_service.get_news_count_by_source()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar estatísticas: {str(e)}")

@router.get("/item/{guid}")
def get_news_by_guid(
    guid: str,
    news_service: NewsService = Depends(get_news_service)
):
    """Retorna uma notícia específica pelo GUID"""
    try:
        all_news = news_service.get_all_news()
        for item in all_news:
            if item.guid == guid:
                return {
                    "title": item.title,
                    "link": item.link,
                    "guid": item.guid,
                    "pub_date": item.pub_date,
                    "description": item.description,
                    "content_encoded": item.content_encoded,
                    "source_url": item.source_url,
                    "source_name": item.source_name,
                    "media_content": item.media_content,
                    "media_thumbnail": item.media_thumbnail,
                    "media_description": item.media_description,
                    "categories": item.categories
                }
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notícia: {str(e)}")