import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import config

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class NewsTelegramBot:
    def __init__(self, api_base: str, telegram_token: str):
        self.api_base = api_base
        self.telegram_token = telegram_token
        self.application = None
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Envia mensagem de boas-vindas quando o comando /start é issued."""
        user = update.effective_user
        welcome_text = (
            f"🤖 Olá {user.first_name}!\n\n"
            "📰 *Sou seu Bot de Notícias* 🤖\n\n"
            "💡 *Comandos disponíveis:*\n"
            "/start - Iniciar bot\n"
            "/noticias - Últimas notícias (rápido)\n"
            "/digest - Resumo diário completo\n"
            "/urgentes - Notícias urgentes\n"
            "/buscar <termo> - Buscar notícias\n"
            "/categorias - Listar categorias\n"
            "/estatisticas - Estatísticas do dia\n"
            "/ajuda - Ajuda e comandos\n\n"
            "🔍 *Exemplos:*\n"
            "/buscar tecnologia\n"
            "/buscar política\n"
            "/digest 10"
        )
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Envia mensagem de ajuda."""
        help_text = (
            "📋 *Comandos do Bot de Notícias*\n\n"
            "📰 /noticias - 3 notícias rápidas\n"
            "📊 /digest [número] - Resumo diário (padrão: 5 notícias)\n"
            "🚨 /urgentes - Notícias das últimas 2 horas\n"
            "🔍 /buscar <termo> - Buscar notícias\n"
            "📂 /categorias - Lista categorias disponíveis\n"
            "📈 /estatisticas - Estatísticas do dia\n"
            "❓ /ajuda - Mostra esta mensagem\n\n"
            "💡 *Dica:* Use /buscar seguido do termo, ex: /buscar esportes"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def send_daily_digest(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Envia resumo diário"""
        try:
            # Verifica se foi passado um número como parâmetro
            limit = 5
            if context.args:
                try:
                    limit = int(context.args[0])
                    limit = min(limit, 15)  # Limite máximo de 15 notícias
                except ValueError:
                    await update.message.reply_text("❌ Por favor, use um número válido. Ex: /digest 5")
                    return
            
            chat_id = update.effective_chat.id
            await update.message.reply_text(f"📊 Buscando resumo diário com {limit} notícias...")
            
            response = requests.get(f"{self.api_base}/telegram/digest?limit={limit}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data["total_count"] > 0:
                    for i, message_data in enumerate(data["messages"], 1):
                        await update.message.reply_text(
                            text=message_data["text"],
                            parse_mode=message_data.get("parse_mode", "HTML"),
                            disable_web_page_preview=message_data.get("disable_web_page_preview", False)
                        )
                    
                    await update.message.reply_text(f"✅ Resumo completo! {data['total_count']} notícias enviadas.")
                else:
                    await update.message.reply_text("❌ Nenhuma notícia encontrada para hoje.")
            else:
                await update.message.reply_text("❌ Erro ao buscar notícias. Tente novamente mais tarde.")
                
        except Exception as e:
            logger.error(f"Erro em send_daily_digest: {e}")
            await update.message.reply_text("❌ Erro interno do bot. Tente novamente.")
    
    async def handle_search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Processa comando de busca"""
        if not context.args:
            await update.message.reply_text(
                "🔍 *Como usar:*\n/buscar <termo de busca>\n\n*Exemplo:*\n/buscar tecnologia\n/buscar política internacional",
                parse_mode='Markdown'
            )
            return
        
        search_term = " ".join(context.args)
        chat_id = update.effective_chat.id
        
        try:
            await update.message.reply_text(f"🔍 Buscando notícias sobre: '{search_term}'...")
            
            response = requests.get(f"{self.api_base}/telegram/search?q={search_term}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data["total_count"] > 0:
                    for i, message_data in enumerate(data["messages"], 1):
                        await update.message.reply_text(
                            text=message_data["text"],
                            parse_mode=message_data.get("parse_mode", "HTML"),
                            disable_web_page_preview=message_data.get("disable_web_page_preview", False)
                        )
                    
                    await update.message.reply_text(f"✅ Busca concluída! {data['total_count']} resultados encontrados.")
                else:
                    await update.message.reply_text(f"❌ Nenhuma notícia encontrada para: '{search_term}'")
            else:
                await update.message.reply_text("❌ Erro na busca. Tente novamente mais tarde.")
                
        except Exception as e:
            logger.error(f"Erro em handle_search_command: {e}")
            await update.message.reply_text("❌ Erro interno do bot. Tente novamente.")
    
    async def send_quick_news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Notícias rápidas"""
        try:
            chat_id = update.effective_chat.id
            await update.message.reply_text("📰 Buscando últimas notícias...")
            
            response = requests.get(f"{self.api_base}/telegram/quick?limit=3")
            
            if response.status_code == 200:
                data = response.json()
                
                for message_data in data["messages"]:
                    await update.message.reply_text(
                        text=message_data["text"],
                        parse_mode=message_data.get("parse_mode"),
                        disable_web_page_preview=message_data.get("disable_web_page_preview", True)
                    )
                
                await update.message.reply_text("📖 Use /digest para mais notícias ou /buscar para pesquisar.")
            else:
                await update.message.reply_text("❌ Erro ao buscar notícias. Tente novamente mais tarde.")
                
        except Exception as e:
            logger.error(f"Erro em send_quick_news: {e}")
            await update.message.reply_text("❌ Erro interno do bot. Tente novamente.")
    
    async def get_categories(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Lista categorias disponíveis"""
        try:
            await update.message.reply_text("📂 Buscando categorias...")
            
            response = requests.get(f"{self.api_base}/news/categories")
            
            if response.status_code == 200:
                categories = response.json()
                
                if categories:
                    categories_text = "📂 *Categorias Disponíveis:*\n\n"
                    for i, category in enumerate(categories[:15], 1):  # Limita a 15 categorias
                        categories_text += f"• {category}\n"
                    
                    if len(categories) > 15:
                        categories_text += f"\n... e mais {len(categories) - 15} categorias"
                    
                    categories_text += "\n\n💡 *Use:* /buscar <categoria> para filtrar"
                    
                    await update.message.reply_text(categories_text, parse_mode='Markdown')
                else:
                    await update.message.reply_text("❌ Nenhuma categoria encontrada.")
            else:
                await update.message.reply_text("❌ Erro ao buscar categorias.")
                
        except Exception as e:
            logger.error(f"Erro em get_categories: {e}")
            await update.message.reply_text("❌ Erro interno do bot.")
    
    async def get_breaking_news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Notícias urgentes"""
        try:
            await update.message.reply_text("🚨 Buscando notícias urgentes...")
            
            response = requests.get(f"{self.api_base}/telegram/breaking")
            
            if response.status_code == 200:
                data = response.json()
                
                if data["total_count"] > 0:
                    for message_data in data["messages"]:
                        await update.message.reply_text(
                            text=message_data["text"],
                            parse_mode=message_data.get("parse_mode", "HTML"),
                            disable_web_page_preview=message_data.get("disable_web_page_preview", False)
                        )
                    
                    await update.message.reply_text(f"🚨 {data['total_count']} notícias urgentes encontradas.")
                else:
                    await update.message.reply_text("✅ Nenhuma notícia urgente no momento.")
            else:
                await update.message.reply_text("❌ Erro ao buscar notícias urgentes.")
                
        except Exception as e:
            logger.error(f"Erro em get_breaking_news: {e}")
            await update.message.reply_text("❌ Erro interno do bot.")
    
    async def get_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Estatísticas do dia"""
        try:
            await update.message.reply_text("📊 Coletando estatísticas...")
            
            response = requests.get(f"{self.api_base}/telegram/stats")
            
            if response.status_code == 200:
                data = response.json()
                await update.message.reply_text(
                    text=data["text"],
                    parse_mode=data.get("parse_mode", "HTML")
                )
            else:
                await update.message.reply_text("❌ Erro ao buscar estatísticas.")
                
        except Exception as e:
            logger.error(f"Erro em get_stats: {e}")
            await update.message.reply_text("❌ Erro interno do bot.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Responde a mensagens que não são comandos"""
        text = update.message.text
        await update.message.reply_text(
            "🤖 Eu sou um bot de notícias! Use os comandos:\n\n"
            "/start - Iniciar\n"
            "/noticias - Notícias rápidas\n"
            "/digest - Resumo diário\n"
            "/ajuda - Ver todos os comandos",
            parse_mode='Markdown'
        )
    
    def setup_handlers(self):
        """Configura os handlers de comandos"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("ajuda", self.help_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("noticias", self.send_quick_news))
        self.application.add_handler(CommandHandler("digest", self.send_daily_digest))
        self.application.add_handler(CommandHandler("urgentes", self.get_breaking_news))
        self.application.add_handler(CommandHandler("buscar", self.handle_search_command))
        self.application.add_handler(CommandHandler("categorias", self.get_categories))
        self.application.add_handler(CommandHandler("estatisticas", self.get_stats))
        
        # Mensagens normais
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    def run(self):
        """Inicia o bot"""
        self.application = Application.builder().token(self.telegram_token).build()
        
        self.setup_handlers()
        
        logger.info("Bot iniciado! Pressione Ctrl+C para parar.")
        self.application.run_polling()

def main():
    # Verifica se o token está configurado
    if not config.TELEGRAM_BOT_TOKEN:
        print("❌ ERRO: TELEGRAM_BOT_TOKEN não configurado!")
        print("1. Crie um bot com @BotFather no Telegram")
        print("2. Adicione TELEGRAM_BOT_TOKEN=seu_token no arquivo .env")
        return
    
    if not config.API_BASE_URL:
        print("❌ ERRO: API_BASE_URL não configurado!")
        print("Certifique-se de que a API FastAPI está rodando")
        return
    
    print(f"🤖 Iniciando Bot de Notícias")
    print(f"🔗 API: {config.API_BASE_URL}")
    
    bot = NewsTelegramBot(
        api_base=config.API_BASE_URL,
        telegram_token=config.TELEGRAM_BOT_TOKEN
    )
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar bot: {e}")

if __name__ == "__main__":
    main()