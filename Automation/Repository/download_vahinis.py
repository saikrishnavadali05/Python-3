import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://sssbpt.info/vahinis/"
BASE_DIR = "vahinis_download"

visited = set()
os.makedirs(BASE_DIR, exist_ok=True)

def download_file(file_url):
    parsed = urlparse(file_url)
    relative_path = parsed.path.replace("/vahinis/", "").lstrip("/")
    local_path = os.path.join(BASE_DIR, relative_path)

    if os.path.exists(local_path):
        print(f"Already exists: {local_path}")
        return

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    print(f"Downloading: {file_url}")
    r = requests.get(file_url, stream=True)
    r.raise_for_status()

    with open(local_path, "wb") as f:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)

def crawl(url):
    if url in visited:
        return
    visited.add(url)

    print(f"\nCrawling: {url}")
    r = requests.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a"):
        href = a.get("href")

        if not href or href.startswith("?") or href == "../":
            continue

        full_url = urljoin(url, href)

        # If it's a directory → recurse
        if href.endswith("/"):
            crawl(full_url)

        else:
            download_file(full_url)

# Start crawling
crawl(BASE_URL)