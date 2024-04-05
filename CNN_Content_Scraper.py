import csv
import os
import scrapy
import time
from scrapy.crawler import CrawlerProcess

class ArticleSpider(scrapy.Spider):
    name = 'article_spider'
    custom_settings = {
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'FEEDS': {
            'scraped_articles.csv': {
                'format': 'csv',
                'encoding': 'utf8',
                'fields': ['date', 'heading', 'article_content'],
            },
        },
        'LOG_LEVEL': 'WARNING',
        'CONCURRENT_REQUESTS': 100,
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self):
        
        self.processed_urls = 0
        self.skipped_urls = 0
        self.total_urls = 0
        self.log_interval = 1  # Log progress every 100 articles

    def start_requests(self):
        input_file = 'all_links_test.txt'
        with open(input_file, 'r', encoding='utf-8') as f:
            urls = [url.strip() for url in f.readlines() if url.strip()]

        self.total_urls = len(urls)
        for url in urls:
            # Ensures each URL ends with .html, as per your requirement
            formatted_url = url.split('.html', 1)[0] + '.html'
            yield scrapy.Request(formatted_url, callback=self.parse_article, errback=self.handle_error)

    def parse_article(self, response):
        self.processed_urls += 1
        if self.processed_urls % self.log_interval == 0 or self.processed_urls == self.total_urls:
            self.log_progress()

        date_text = response.xpath("//meta[@property='article:published_time']/@content").get(default='N/A').strip()
        # Updated XPath for heading
        heading_text = response.xpath('/html/body/div[2]/section[3]/div/div[1]/h1/text()').get(default='N/A').strip()
        paragraphs = response.css('div.article__content p::text').getall()
        article_content = '\n'.join(paragraphs).strip()

        yield {
            'date': date_text,
            'heading': heading_text,
            'article_content': article_content
        }

    def handle_error(self, failure):
        self.skipped_urls += 1
        self.log_progress()

    def log_progress(self):
        
        print(f'Processed: {self.processed_urls}/{self.total_urls}, Skipped: {self.skipped_urls}.', end='\r')

def scrape_articles_from_file(input_file):
    process = CrawlerProcess()
    process.crawl(ArticleSpider)
    process.start()

if __name__ == "__main__":
    scrape_articles_from_file('all_links_test.txt')
