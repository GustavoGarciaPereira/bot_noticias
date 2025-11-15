from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

class NewsItem:
    """Modelo de domínio expandido para notícia"""
    
    def __init__(
        self, 
        title: str,
        link: str,
        guid: str,
        pub_date: datetime,
        description: Optional[str] = None,
        content_encoded: Optional[str] = None,
        source_url: Optional[str] = None,
        source_name: Optional[str] = None,
        media_content: Optional[List[Dict]] = None,
        media_thumbnail: Optional[str] = None,
        media_description: Optional[str] = None,
        categories: Optional[List[str]] = None,
        raw_data: Optional[Dict[str, Any]] = None
    ):
        self.title = title
        self.link = link
        self.guid = guid
        self.pub_date = pub_date
        self.description = description
        self.content_encoded = content_encoded
        self.source_url = source_url
        self.source_name = source_name
        self.media_content = media_content or []
        self.media_thumbnail = media_thumbnail
        self.media_description = media_description
        self.categories = categories or []
        self.raw_data = raw_data or {}