from typing import List, Dict, Any
from app.services.news_service import NewsService
from app.models.news import NewsItem
from app.schemas.telegram import TelegramNewsItem, TelegramNewsMessage, TelegramNewsList

class TelegramService:
    """Serviço especializado em formatar notícias para Telegram"""
    
    def __init__(self, news_service: NewsService):
        self.news_service = news_service
    
    def format_news_for_telegram(self, news_item: NewsItem) -> str:
        """Formata uma única notícia para mensagem do Telegram"""
        # Limita o título para não ficar muito longo no Telegram
        title = news_item.title
        if len(title) > 200:
            title = title[:197] + "..."
        
        # Escapa caracteres especiais para HTML
        title = self.escape_html(title)
        source = self.escape_html(news_item.source_name or "Fonte Desconhecida")
        
        message = f"📰 <b>{title}</b>\n\n"
        message += f"📊 <i>Fonte: {source}</i>\n"
        
        if news_item.pub_date:
            date_str = news_item.pub_date.strftime("%d/%m/%Y %H:%M")
            message += f"🕐 <i>Publicado: {date_str}</i>\n"
        
        message += f"\n🔗 <a href='{news_item.link}'>Ler notícia completa</a>"
        
        return message
    
    def escape_html(self, text: str) -> str:
        """Escapa caracteres especiais para formato HTML do Telegram"""
        escape_chars = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }
        for char, replacement in escape_chars.items():
            text = text.replace(char, replacement)
        return text
    
    def get_daily_digest(self, limit: int = 10) -> TelegramNewsList:
        """Retorna resumo diário de notícias"""
        today_news = self.news_service.get_todays_news()[:limit]
        
        messages = []
        for i, news_item in enumerate(today_news, 1):
            message_text = f"<b>📊 RESUMO DIÁRIO ({i}/{len(today_news)})</b>\n\n"
            message_text += self.format_news_for_telegram(news_item)
            
            messages.append(TelegramNewsMessage(
                text=message_text,
                parse_mode="HTML",
                disable_web_page_preview=False
            ))
        
        return TelegramNewsList(
            messages=messages,
            total_count=len(today_news)
        )
    
    def search_news_for_telegram(self, search_term: str, limit: int = 5) -> TelegramNewsList:
        """Busca notícias e formata para Telegram"""
        from app.schemas.news import NewsSearchFilters
        
        filters = NewsSearchFilters(search_term=search_term)
        results = self.news_service.search_news(filters)[:limit]
        
        messages = []
        if results:
            for i, news_item in enumerate(results, 1):
                message_text = f"<b>🔍 RESULTADO {i}/{len(results)}</b>\n\n"
                message_text += self.format_news_for_telegram(news_item)
                
                messages.append(TelegramNewsMessage(
                    text=message_text,
                    parse_mode="HTML",
                    disable_web_page_preview=False
                ))
        else:
            messages.append(TelegramNewsMessage(
                text="❌ <b>Nenhuma notícia encontrada para sua busca.</b>\n\nTente outros termos de pesquisa.",
                parse_mode="HTML"
            ))
        
        return TelegramNewsList(
            messages=messages,
            total_count=len(results)
        )
    
    def get_news_by_category_telegram(self, category: str, limit: int = 5) -> TelegramNewsList:
        """Notícias por categoria formatadas para Telegram"""
        news_items = self.news_service.get_news_by_category(category)[:limit]
        
        messages = []
        if news_items:
            for i, news_item in enumerate(news_items, 1):
                message_text = f"<b>📂 {category.upper()} - {i}/{len(news_items)}</b>\n\n"
                message_text += self.format_news_for_telegram(news_item)
                
                messages.append(TelegramNewsMessage(
                    text=message_text,
                    parse_mode="HTML",
                    disable_web_page_preview=False
                ))
        else:
            messages.append(TelegramNewsMessage(
                text=f"❌ <b>Nenhuma notícia encontrada na categoria '{category}'.</b>",
                parse_mode="HTML"
            ))
        
        return TelegramNewsList(
            messages=messages,
            total_count=len(news_items)
        )
    
    def get_breaking_news(self, limit: int = 3) -> TelegramNewsList:
        """Notícias mais recentes (últimas 2 horas)"""
        from datetime import datetime, timedelta
        
        all_news = self.news_service.get_all_news()
        two_hours_ago = datetime.now() - timedelta(hours=2)
        
        breaking_news = [
            item for item in all_news 
            if item.pub_date and item.pub_date > two_hours_ago
        ][:limit]
        
        messages = []
        for i, news_item in enumerate(breaking_news, 1):
            message_text = "🚨 <b>NOTÍCIA URGENTE</b> 🚨\n\n"
            message_text += self.format_news_for_telegram(news_item)
            
            messages.append(TelegramNewsMessage(
                text=message_text,
                parse_mode="HTML",
                disable_web_page_preview=False
            ))
        
        return TelegramNewsList(
            messages=messages,
            total_count=len(breaking_news)
        )
    
    def get_news_stats_telegram(self) -> str:
        """Estatísticas formatadas para Telegram"""
        all_news = self.news_service.get_all_news()
        sources_count = self.news_service.get_news_count_by_source()
        categories = self.news_service.get_news_categories()
        
        total_news = len(all_news)
        total_sources = len(sources_count)
        total_categories = len(categories)
        
        # Notícias de hoje
        today_news = self.news_service.get_todays_news()
        
        stats_text = "📊 <b>ESTATÍSTICAS DO DIA</b>\n\n"
        stats_text += f"📰 <b>Total de notícias:</b> {total_news}\n"
        stats_text += f"📈 <b>Notícias de hoje:</b> {len(today_news)}\n"
        stats_text += f"🏢 <b>Fontes:</b> {total_sources}\n"
        stats_text += f"📂 <b>Categorias:</b> {total_categories}\n\n"
        
        # Top fontes
        stats_text += "<b>🔝 TOP FONTES:</b>\n"
        for source, count in list(sources_count.items())[:5]:
            stats_text += f"• {source}: {count} notícias\n"
        
        return stats_text