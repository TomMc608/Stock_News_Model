import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_articles_from_file(input_file):
    with open(input_file, 'r') as file:
        urls = file.readlines()

    articles_data = []
    total_urls = len(urls)
    for index, url in enumerate(urls, start=1):
        url = url.strip()  # Remove leading/trailing whitespaces and newlines
        print(f"Scraping article {index} of {total_urls}...")
        article_data = scrape_article(url)
        articles_data.append(article_data)
        print("Article scraped successfully.\n")
        time.sleep(1)  # Adding a delay to be polite to the server

    return articles_data

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the article content container
        article_container = soup.find('div', class_='article__content-container')

        if article_container:
            # Exclude specified elements from the article content
            for unwanted_element in article_container.select('div.gallery-inline, div.related-content.related-content--article > a'):
                unwanted_element.extract()

            # Extract text content from the modified article container
            article_text = article_container.get_text(separator='\n')

            # Format the article text for better readability
            formatted_article = format_article(article_text)
            return {'url': url, 'content': formatted_article}
        else:
            print("Article container not found on the page:", url)
            return {'url': url, 'content': 'Not found'}

    except requests.exceptions.RequestException as e:
        print("Error fetching the page:", e)
        return {'url': url, 'content': 'Error'}

def format_article(article_text):
    # Remove excess newlines and whitespace
    formatted_text = '\n'.join(line.strip() for line in article_text.split('\n') if line.strip())
    return formatted_text

def save_articles_to_csv(articles_data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['url', 'content'])
        writer.writeheader()
        writer.writerows(articles_data)

if __name__ == '__main__':
    input_file = 'output_article_links.txt'  # Change this to the path of your input file
    output_file = 'scraped_articles.csv'

    articles_data = scrape_articles_from_file(input_file)
    save_articles_to_csv(articles_data, output_file)
    print("Articles saved to 'scraped_articles.csv'")
