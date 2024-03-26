import requests
from bs4 import BeautifulSoup
import csv
import time
import os
from requests import Session
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_articles_from_file(input_file, output_file='scraped_articles.csv', max_workers=10):
    # Create an empty CSV file if it doesn't exist
    if not os.path.exists(output_file):
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'heading', 'article_content'])
            writer.writeheader()

    with open(input_file, 'r', encoding='utf-8') as file:
        urls = file.readlines()


    failed_urls = 0
    articles_data = []
    total_urls = len(urls)
    start_time = time.time()  # Record the start time

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit scraping tasks for each URL
        future_to_url = {executor.submit(scrape_article_with_retry, url.strip().split(".html")[0] + ".html"): url for url in urls}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                article_data = future.result()
                if article_data:
                    articles_data.append(article_data)
            except Exception as e:
               # print(f"Error occurred while scraping URL {url}: {e}")
                failed_urls += 1

            # Print progress after processing each URL
            print_progress(len(articles_data), total_urls, start_time)

    # Save all articles to CSV after all URLs have been processed
    save_articles_to_csv(articles_data, output_file)

    print(f"\nAll articles scraped and saved successfully! Failed on {failed_urls} URLs.")




def scrape_article_with_retry(url, max_retries=1):
    retries = 0
    while retries <= max_retries:
        try:
            article_data = scrape_article(url)
            if article_data:
                return article_data
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            retries += 1
            if retries > max_retries:
                break
    print(f"Failed to scrape URL: {url} after {max_retries} retries.")
    return None

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.HTTPError as e:
        print(f"HTTP error occurred while fetching {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting date
    date_container = soup.select_one('body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__top.layout-with-rail__top > div > div.headline__footer > div.headline__sub-container > div > div.headline__byline-sub-text > div.timestamp')
    date_text = date_container.get_text(strip=True) if date_container else 'N/A'

    # Extracting heading
    heading_container = soup.select_one('body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__top.layout-with-rail__top > div > div.headline__wrapper')
    heading_text = heading_container.get_text(strip=True) if heading_container else 'N/A'

    # Extracting article content
    base_container = soup.select_one('body > div.layout__content-wrapper.layout-with-rail__content-wrapper > section.layout__wrapper.layout-with-rail__wrapper > section.layout__main-wrapper.layout-with-rail__main-wrapper > section.layout__main.layout-with-rail__main > article > section > main > div.article__content-container > div.article__content')

    # Extract all text content within the base container and its subcontainers
    all_text = ''
    if base_container:
        for element in base_container.descendants:
            if element.name == 'p':  # Consider only paragraph elements
                all_text += element.get_text(strip=True) + '\n'

    return {'date': date_text, 'heading': heading_text, 'article_content': all_text}


def save_articles_to_csv(articles_data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:  
        writer = csv.DictWriter(file, fieldnames=['date', 'heading', 'article_content'])
        writer.writeheader()
        writer.writerows(articles_data)


def print_progress(current, total, start_time):
    elapsed_time = time.time() - start_time
    progress_percentage = (current / total) * 100
    eta_seconds = (elapsed_time / current) * (total - current) if current != 0 else 0
    eta_minutes = int(eta_seconds // 60)
    eta_seconds %= 60
    print(f"\rProgress: {progress_percentage:.2f}% | ETA: {eta_minutes}m {int(eta_seconds)}s", end="")

if __name__ == "__main__":
    scrape_articles_from_file('all_links_test.txt')
