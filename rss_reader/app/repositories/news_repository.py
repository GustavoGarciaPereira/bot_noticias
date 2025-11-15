import requests
import xmltodict
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.config import settings
from app.models.news import NewsItem

class NewsRepository:
    """Repositório expandido para RSS Feed"""
    
    def __init__(self):
        self.feed_url = settings.RSS_FEED_URL
    
    def fetch_raw_news_data(self) -> List[Dict[str, Any]]:
        try:
            response = requests.get(self.feed_url, timeout=10)
            response.raise_for_status()
            news_data = xmltodict.parse(response.content)
            
            items = news_data.get("rss", {}).get("channel", {}).get("item", [])
            return items if isinstance(items, list) else [items]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao buscar dados do RSS: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao processar RSS feed: {str(e)}")
    
    def parse_datetime(self, date_str: str) -> datetime:
        """Converte string de data do RSS para datetime"""
        formats = [
            "%a, %d %b %Y %H:%M:%S %Z",
            "%a, %d %b %Y %H:%M:%S %z",
            "%Y-%m-%dT%H:%M:%SZ"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return datetime.now()
    
    def extract_media_content(self, item: Dict) -> List[Dict]:
        """Extrai informações de mídia do item"""
        media_content = []
        
        # Media content
        media = item.get("media:content")
        if media:
            if isinstance(media, list):
                for m in media:
                    media_content.append({
                        "url": m.get("@url"),
                        "medium": m.get("@medium"),
                        "width": int(m.get("@width", 0)),
                        "height": int(m.get("@height", 0))
                    })
            elif isinstance(media, dict):
                media_content.append({
                    "url": media.get("@url"),
                    "medium": media.get("@medium"),
                    "width": int(media.get("@width", 0)),
                    "height": int(media.get("@height", 0))
                })
        
        return media_content
    
    def extract_categories(self, item: Dict) -> List[str]:
        """Extrai categorias do item"""
        categories = []
        category = item.get("category")
        
        if category:
            if isinstance(category, list):
                categories.extend([cat.get("#text", cat) if isinstance(cat, dict) else cat for cat in category])
            elif isinstance(category, dict):
                categories.append(category.get("#text", ""))
            else:
                categories.append(category)
        
        return categories
    
    def get_news_items(self) -> List[NewsItem]:
        """Retorna lista completa de NewsItems"""
        raw_items = self.fetch_raw_news_data()
        news_items = []
        
        for item in raw_items:
            # Processa source
            source = item.get("source", {})
            source_url = source.get("@url") if isinstance(source, dict) else None
            source_name = source.get("#text") if isinstance(source, dict) else source
            
            # Processa data
            pub_date_str = item.get("pubDate", "")
            pub_date = self.parse_datetime(pub_date_str)
            
            # Processa mídia
            media_content = self.extract_media_content(item)
            media_thumbnail = item.get("media:thumbnail", {}).get("@url") if isinstance(item.get("media:thumbnail"), dict) else None
            media_description = item.get("media:description")
            
            # Processa categorias
            categories = self.extract_categories(item)
            
            news_item = NewsItem(
                title=item.get("title", ""),
                link=item.get("link", ""),
                guid=item.get("guid", ""),
                pub_date=pub_date,
                description=item.get("description"),
                content_encoded=item.get("content:encoded"),
                source_url=source_url,
                source_name=source_name,
                media_content=media_content,
                media_thumbnail=media_thumbnail,
                media_description=media_description,
                categories=categories,
                raw_data=item
            )
            news_items.append(news_item)
        
        return news_items