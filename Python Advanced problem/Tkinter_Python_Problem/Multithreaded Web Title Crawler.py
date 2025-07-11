#pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of websites to crawl
urls = [
    "https://www.python.org",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.wikipedia.org",
    "https://www.openai.com",
    "https://www.reddit.com"
]

def fetch_title(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise for bad status
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'No title found'
        return (url, title)
    except Exception as e:
        return (url, f"Error: {e}")

def crawl_sites(url_list, max_workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_title, url): url for url in url_list}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append((url, f"Exception: {e}"))
    return results

# Run the crawler
if __name__ == "__main__":
    titles = crawl_sites(urls)
    for url, title in titles:
        print(f"{url}: {title}")
