import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

BASE_URL = "https://oceansofgamess.com/"

def check_robots(url):
    robots_url = urljoin(url, "/robots.txt")
    try:
        r = requests.get(robots_url, timeout=10)
        if r.status_code == 200:
            print("[INFO] robots.txt found:")
            print(r.text)
        else:
            print("[INFO] No robots.txt found or not accessible (status:", r.status_code, ")")
    except Exception as e:
        print("[ERROR] Failed to fetch robots.txt:", e)

def crawl_page(url):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
    except Exception as e:
        print("[ERROR] Failed to fetch page:", e)
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(url, href)
        if urlparse(full_url).netloc == urlparse(BASE_URL).netloc:
            links.add(full_url)

    return links

if __name__ == "__main__":
    print("=== Checking robots.txt ===")
    check_robots(BASE_URL)

    print("\n=== Crawling main page ===")
    found_links = crawl_page(BASE_URL)

    print(f"[INFO] Found {len(found_links)} links:")
    for link in found_links:
        print(link)

    # Save to file
    with open("oceans_links.txt", "w", encoding="utf-8") as f:
        for link in found_links:
            f.write(link + "\n")

    print("\n[INFO] Saved links to oceans_links.txt")
