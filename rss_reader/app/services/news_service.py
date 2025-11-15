from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.repositories.news_repository import NewsRepository
from app.models.news import NewsItem
from app.schemas.news import NewsItemResponse, NewsSearchFilters

class NewsService:
    """Serviço expandido com novas funcionalidades"""
    
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository
    
    def get_all_news(self) -> List[NewsItem]:
        return self.news_repository.get_news_items()
    
    def get_news_with_formatted_response(self) -> List[Dict[str, Any]]:
        news_items = self.get_all_news()
        
        formatted_items = []
        for item in news_items:
            formatted_item = {
                "title": item.title,
                "link": item.link,
                "guid": item.guid,
                "pub_date": item.pub_date,
                "description": item.description,
                "source_url": item.source_url,
                "source_name": item.source_name,
                "media_content": item.media_content,
                "media_thumbnail": item.media_thumbnail,
                "categories": item.categories
            }
            formatted_items.append(formatted_item)
        
        return formatted_items
    
    def search_news(self, filters: NewsSearchFilters) -> List[NewsItem]:
        """Busca notícias com filtros"""
        all_news = self.get_all_news()
        filtered_news = all_news
        
        # Filtro por categoria
        if filters.category:
            filtered_news = [item for item in filtered_news 
                           if filters.category.lower() in [cat.lower() for cat in item.categories]]
        
        # Filtro por fonte
        if filters.source:
            filtered_news = [item for item in filtered_news 
                           if item.source_name and filters.source.lower() in item.source_name.lower()]
        
        # Filtro por data
        if filters.date_from:
            filtered_news = [item for item in filtered_news 
                           if item.pub_date >= filters.date_from]
        
        if filters.date_to:
            filtered_news = [item for item in filtered_news 
                           if item.pub_date <= filters.date_to]
        
        # Filtro por termo de busca
        if filters.search_term:
            term = filters.search_term.lower()
            filtered_news = [item for item in filtered_news 
                           if (term in item.title.lower() or 
                               (item.description and term in item.description.lower()))]
        
        return filtered_news
    
    def get_news_by_category(self, category: str) -> List[NewsItem]:
        """Filtra notícias por categoria"""
        all_news = self.get_all_news()
        return [item for item in all_news 
                if category.lower() in [cat.lower() for cat in item.categories]]
    
    def get_todays_news(self) -> List[NewsItem]:
        """Retorna notícias de hoje"""
        all_news = self.get_all_news()
        today = datetime.now().date()
        return [item for item in all_news 
                if item.pub_date.date() == today]
    
    def get_news_sources(self) -> List[str]:
        """Retorna lista de fontes únicas"""
        all_news = self.get_all_news()
        sources = set(item.source_name for item in all_news if item.source_name)
        return sorted(list(sources))
    
    def get_news_categories(self) -> List[str]:
        """Retorna lista de categorias únicas"""
        all_news = self.get_all_news()
        categories = set()
        for item in all_news:
            categories.update(item.categories)
        return sorted(list(categories))
    
    def get_news_with_images(self) -> List[NewsItem]:
        """Retorna notícias que possuem imagens"""
        all_news = self.get_all_news()
        return [item for item in all_news 
                if item.media_content or item.media_thumbnail]
    
    def get_news_count_by_source(self) -> Dict[str, int]:
        """Retorna contagem de notícias por fonte"""
        all_news = self.get_all_news()
        count_dict = {}
        for item in all_news:
            if item.source_name:
                count_dict[item.source_name] = count_dict.get(item.source_name, 0) + 1
        return count_dict