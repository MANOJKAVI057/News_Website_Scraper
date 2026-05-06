import requests
import json
import datetime
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time

# --- Config ---
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://timesofindia.indiatimes.com/"


def safe_request(url, retries=3):
    """Safe request with retry."""
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            return r
        except Exception as e:
            print(f"[WARN] Retry {i+1} failed for {url}: {e}")
            time.sleep(2)
    return None


def scrape_home(url):
    """Scrape homepage headlines."""
    r = safe_request(url)
    if not r:
        return []

    soup = BeautifulSoup(r.text, "lxml")

    # Better selectors (TOI updated structure)
    articles = soup.select("a[href*='/articleshow/']")

    seen = set()
    results = []

    for a in articles:
        title = a.get_text(strip=True)
        link = a.get("href")

        if not title or not link:
            continue

        # Make full URL
        link = urljoin(BASE_URL, link)

        # Remove duplicates
        if link in seen:
            continue
        seen.add(link)

        results.append({
            "title": title,
            "link": link
        })

    return results


def scrape_article(url):
    """Scrape article content."""
    r = safe_request(url)
    if not r:
        return ""

    soup = BeautifulSoup(r.text, "lxml")

    # Updated selectors (TOI uses multiple structures)
    paragraphs = soup.select("div._s30J.clearfix p, div.Normal p, div[data-articlebody] p")

    content = " ".join(p.get_text(" ", strip=True) for p in paragraphs)

    return content


def run():
    print("[INFO] Scraping homepage...")

    headlines = scrape_home(BASE_URL)

    if not headlines:
        print(" No data fetched")
        return

    print(f"[INFO] Found {len(headlines)} headlines")

    submission = []

    for item in headlines[:20]:
        print(f"[INFO] Fetching: {item['title'][:50]}")

        content = scrape_article(item["link"])
        item["content"] = content

        submission.append(item)
        time.sleep(1)  # polite delay

    # Save JSON
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"toi_{today}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(submission, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Saved {filename}")

    # Convert to DataFrame
    df = pd.DataFrame(submission)

    print("\n=== Headlines & Links ===")
    for _, row in df.iterrows():
        print(f"{row['title'][:60]} | {row['link']}")


if __name__ == "__main__":
    run()