import requests
from bs4 import BeautifulSoup
from newspaper import Article


def get_article_text(url: str) -> str:
    # First try newspaper3k
    try:
        article = Article(url)
        article.download()
        article.parse()

        text = " ".join(article.text.split())

        if text:
            return text
    except Exception:
        pass

    # Fallback: selective BeautifulSoup extraction. this is just in case newspaper fails to parse properly
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove junk elements
    for tag in soup(["script", "style", "noscript", "svg", "img", "figure", "aside", "footer", "nav", "form"]):
        tag.decompose()

    # Prefer semantic article/main containers
    container = soup.find("article") or soup.find("main") or soup.body

    if container is None:
        raise ValueError("No article text could be extracted from the provided URL.")

    paragraphs = container.find_all("p")
    text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
    text = " ".join(text.split())

    if not text:
        raise ValueError("No article text could be extracted from the provided URL.")

    return text