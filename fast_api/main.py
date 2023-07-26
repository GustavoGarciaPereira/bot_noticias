from fastapi import FastAPI
import requests
import xmltodict


app = FastAPI()

url = "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419"


def get_news_from_feed():
    request = requests.get(url)
    news_data = xmltodict.parse(request.content)
    return news_data["rss"]["channel"]["item"]


@app.get("/items")
def get_items_with_urls():
    news_items = get_news_from_feed()
    print(news_items)
    items_with_urls = []

    for item in news_items:
        title = item["title"]
        source_url = item.get("source", {}).get("@url")
        link = item["link"]

        item_info = {"title": title, "source_url": source_url, "link": link}
        items_with_urls.append(item_info)

    return items_with_urls


@app.get("/")
def main():
    return get_news_from_feed()
