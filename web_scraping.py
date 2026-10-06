"""
TASK 1 - Web Scraping
Scrapes publicly accessible demo data from Books to Scrape.
Website: https://books.toscrape.com/
Use responsibly and respect robots.txt, rate limits, and site terms.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
OUTPUT = "data/books_scraped.csv"

rows = []
url = START_URL

for page in range(1, 4):  # first 3 pages for a manageable project dataset
    page_url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(page_url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for article in soup.select("article.product_pod"):
        title = article.h3.a.get("title", "").strip()
        price = article.select_one(".price_color").get_text(strip=True)
        availability = article.select_one(".availability").get_text(" ", strip=True)
        rating = article.p.get("star-rating")
        rating = " ".join(rating.get("class", [])) if rating else ""
        rel_link = article.h3.a.get("href", "")
        product_url = urljoin(page_url, rel_link)

        rows.append({
            "title": title,
            "price_gbp": price.replace("Â£", ""),
            "availability": availability,
            "rating": rating.replace("star-rating ", ""),
            "product_url": product_url
        })

df = pd.DataFrame(rows)
df.to_csv(OUTPUT, index=False)
print(f"Saved {len(df)} records to {OUTPUT}")