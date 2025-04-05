from feedgen.feed import FeedGenerator
from datetime import datetime
import os

def generate_rss(title, body, image_url=None):
    fg = FeedGenerator()
    fg.title("Telegram → Яндекс Дзен")
    fg.link(href="https://t.me/neiro_business")
    fg.description("Автоматические статьи из Telegram")

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href="https://t.me/neiro_business")
    
    content = f"<img src='{image_url}'/><br>{body}" if image_url else body
    fe.description(content)
    fe.pubDate(datetime.now())

    os.makedirs("output", exist_ok=True)
    fg.rss_file("output/rss.xml") 
