from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TelegramNewsItem(BaseModel):
    """Schema otimizado para mensagens no Telegram"""
    title: str
    link: str
    source: Optional[str] = None
    pub_date: Optional[datetime] = None
    has_image: bool = False

class TelegramNewsMessage(BaseModel):
    """Formato de mensagem pronta para o Telegram"""
    text: str
    parse_mode: str = "HTML"
    disable_web_page_preview: bool = False

class TelegramNewsList(BaseModel):
    """Lista de notícias formatada para o Telegram"""
    messages: List[TelegramNewsMessage]
    total_count: int