from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

class MediaContent(BaseModel):
    url: str
    medium: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

class NewsItemBase(BaseModel):
    title: str
    link: str
    guid: str

class NewsItemResponse(NewsItemBase):
    pub_date: datetime
    description: Optional[str] = None
    content_encoded: Optional[str] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    media_content: List[MediaContent] = []
    media_thumbnail: Optional[str] = None
    media_description: Optional[str] = None
    categories: List[str] = []
    
    class Config:
        from_attributes = True

class NewsSearchFilters(BaseModel):
    category: Optional[str] = None
    source: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search_term: Optional[str] = None