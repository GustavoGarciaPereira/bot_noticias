import os
from typing import List

class Settings:
    ALLOWED_ORIGIN: str = os.environ.get("ALLOWED_ORIGIN", "http://localhost:3000")
    RSS_FEED_URL: str = "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419"
    
    @property
    def cors_origins(self) -> List[str]:
        return [self.ALLOWED_ORIGIN]

settings = Settings()