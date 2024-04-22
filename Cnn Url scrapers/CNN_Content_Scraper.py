import csv
import os
import scrapy
import time
from scrapy.crawler import CrawlerProcess

class ArticleSpider(scrapy.Spider):
    name = 'article_spider'
    start_time = time.time()
    processed_urls = 0
    total_urls = 0

    def start_requests(self):
        input_file = 'all_links_test.txt'
        with open(input_file, 'r', encoding='utf-8') as f:
            urls = f.readlines()

        self.total_urls = len(urls)
        for url in urls:
            formatted_url = url.split('.html', 1)[0] + '.html'
            yield scrapy.Request(formatted_url.strip(), callback=self.parse_article)

    def parse_article(self, response):
        self.processed_urls += 1
        elapsed_time = time.time() - self.start_time
        estimated_time = ((elapsed_time / self.processed_urls) * (self.total_urls - self.processed_urls)) / 60
        estimated_time = round(estimated_time, 2)

        print(f'Processed {self.processed_urls}/{self.total_urls}. Estimated time left: {estimated_time} minutes')

        date_text = response.css('div.timestamp::text').get(default='N/A').strip()
        heading_text = response.css('div.headline__wrapper::text').get(default='N/A').strip()
        paragraphs = response.css('div.article__content p::text').getall()
        article_content = '\n'.join(paragraphs)

        yield {
            'date': date_text,
            'heading': heading_text,
            'article_content': article_content
        }

def scrape_articles_from_file(input_file, output_file='scraped_articles.csv'):
    if not os.path.exists(output_file):
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['date', 'heading', 'article_content'])
            writer.writeheader()

    total_scraped_urls = 0

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'csv',
        'FEED_URI': output_file,
        'LOG_LEVEL': 'WARNING',
        'CONCURRENT_REQUESTS': 1
    })

    process.crawl(ArticleSpider)
    process.start()

if __name__ == "__main__":
    scrape_articles_from_file('all_links_test.txt')