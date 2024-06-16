import sys
import requests
from bs4 import BeautifulSoup
import re
import json

def fetch_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.text

def fetch_thread_urls(user_url):
    thread_urls = []

    if '.html' in user_url:
        base_url = user_url[:user_url.rfind('-') + 1]
        start_page = int(user_url[user_url.rfind('-') + 1:-5])

        page_url = f"{base_url}{start_page}.html"
        page_content = fetch_url(page_url)

        match = re.search(r'id="autopbn" totalpage="(\d+)"', page_content)
        if match:
            total_pages = int(match.group(1))
        else:
            total_pages = 1  # 如果没有找到 totalpage，默认只处理当前页面

        for page in range(1, total_pages + 1):
            page_url = f"{base_url}{page}.html"
            page_content = fetch_url(page_url)

            soup = BeautifulSoup(page_content, 'html.parser')
            elements = soup.select('[id^=normalthread] a[href*="thread"]')

            for element in elements:
                href = element.get('href')
                if href and 'thread' in href:
                    parts = href.split('-')
                    if len(parts) > 2 and parts[2] == '1':
                        full_url = f"https://klpbbs.com/{href.lstrip('/')}"
                        if full_url not in thread_urls:
                            thread_urls.append(full_url)
        return thread_urls

    else:
        if 'page=' not in user_url:
            base_url = f"{user_url}&page="
        else:
            base_url = re.sub(r'page=\d+', 'page=', user_url)

        start_page = 1
        total_pages = 0

        page_url = f"{base_url}{start_page}"
        page_content = fetch_url(page_url)

        match = re.search(r'id="autopbn" totalpage="(\d+)"', page_content)
        if match:
            total_pages = int(match.group(1))
        else:
            total_pages = 1  # 如果没有找到 totalpage，默认只处理当前页面

        for page in range(start_page, total_pages + 1):
            page_url = f"{base_url}{page}"
            page_content = fetch_url(page_url)

            soup = BeautifulSoup(page_content, 'html.parser')
            elements = soup.select('[id^=normalthread] a[href*="thread"]')

            for element in elements:
                href = element.get('href')
                if href and 'thread' in href:
                    parts = href.split('-')
                    if len(parts) > 2 and parts[2] == '1':
                        full_url = f"https://klpbbs.com/{href.lstrip('/')}"
                        if full_url not in thread_urls:
                            thread_urls.append(full_url)
        return thread_urls

def main(url):
    thread_urls = fetch_thread_urls(url)

    if thread_urls:
        for thread_url in thread_urls:
            print(thread_url)
    else:
        print("未找到有效链接。")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read.py <url>")
        sys.exit(1)

    user_url = sys.argv[1]
    main(user_url)
