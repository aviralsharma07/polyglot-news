from datetime import datetime

# This is YOUR schema. You own it.
def make_article(title, url, source, published_at, description="", query="", fetched_from=""):
    return {
        "title": title,
        "url": url,
        "source": source,
        "published_at": published_at,   # always a Python datetime object
        "description": description,
        "query": query,
        "fetched_from": fetched_from          # which API gave us this
    }

def from_newsapi(raw, query):
    articles = []
    for item in raw.get("articles", []):
        try:
            pub = datetime.fromisoformat(item["publishedAt"].replace("Z", "+00:00"))
            articles.append(make_article(
                title=item.get("title", ""),
                url=item.get("url", ""),
                source=item.get("source", {}).get("name", "Unknown"),
                published_at=pub,
                description=item.get("description", ""),
                query=query,
                fetched_from="NewsAPI"
            ))
        except Exception as e:
            print(f"[WARN] Skipped article: {e}")
    return articles

def from_gnews(raw, query):
    articles = []
    for item in raw.get("articles", []):
        try:
            pub_raw = item.get("publishedAt") or item.get("published_at") or item.get("date")
            pub = datetime.fromisoformat(pub_raw.replace("Z", "+00:00")) if pub_raw else datetime.utcnow()
            articles.append(make_article(
                title=item.get("title", ""),
                url=item.get("url", ""),
                source=item.get("source", {}).get("name", "Unknown"),
                published_at=pub,
                description=item.get("description", ""),
                query=query,
                fetched_from="GNews"
            ))
        except Exception as e:
            print(f"[WARN] Skipped article: {e}")
    return articles

def from_currentapi(raw, query):
    articles = []
    for item in raw.get("news", []):
        try:
            pub_raw = item.get("publishedAt") or item.get("published_at") or item.get("published") or item.get("pubDate")
            pub = datetime.utcnow()
            if pub_raw:
                pub_text = pub_raw.replace("Z", "+00:00")
                if len(pub_text) >= 5 and pub_text[-5] in "+-" and pub_text[-4:].isdigit():
                    pub_text = pub_text[:-5] + pub_text[-5:-2] + ":" + pub_text[-2:]
                pub = datetime.fromisoformat(pub_text)
            source = item.get("source") or item.get("source_id") or item.get("author") or "Unknown"
            if isinstance(source, dict):
                source = source.get("name", "Unknown")
            articles.append(make_article(
                title=item.get("title", ""),
                url=item.get("url", item.get("link", "")),
                source=source,
                published_at=pub,
                description=item.get("description", item.get("summary", "")),
                query=query,
                fetched_from="CurrentNews"
            ))
        except Exception as e:
            print(f"[WARN] Skipped article: {e}")
    return articles