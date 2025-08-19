import requests
from bs4 import BeautifulSoup

def scrape_company_pages(base_url, extra_paths=None):
    headers = {"User-Agent": "Mozilla/5.0"}
    paths_to_try = [
        "", "/about", "/about-us", "/products", "/services", "/company", "/mission"
    ]
    
    if extra_paths:
        paths_to_try.extend(extra_paths)

    scraped_text = ""

    for path in paths_to_try:
        full_url = base_url.rstrip("/") + path
        try:
            print(f"[Scraper] Trying: {full_url}")
            response = requests.get(full_url, headers=headers, timeout=6)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                scraped_text += " " + text
        except Exception as e:
            print(f"[Scraper] Error fetching {full_url}: {e}")
            continue

    print(f"[Scraper] Total scraped characters: {len(scraped_text)}")
    return scraped_text