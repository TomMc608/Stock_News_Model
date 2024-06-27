import asyncio
import aiohttp
from bs4 import BeautifulSoup
import aiofiles
import pandas as pd
from tqdm.asyncio import tqdm
import os

# File containing the links
links_file = "./nbc_news_links.txt"
# Output CSV file
output_csv = "nbc_news_articles.csv"
# Batch size for saving progress
batch_size = 10

# Function to scrape article content and publication date
async def scrape_article(session, link):
    async with session.get(link) as response:
        if response.status == 200:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            article_content_div = soup.find('div', class_='article-body__content')
            date_time_tag = soup.find('time', class_='relative z-1')
            if article_content_div and date_time_tag:
                paragraphs = article_content_div.find_all('p')
                article_content = "\n".join([p.get_text() for p in paragraphs])
                date_published = date_time_tag['datetime']
                return date_published, article_content
    return None, None

# Function to read links and scrape articles asynchronously
async def scrape_articles_from_links():
    articles = []
    async with aiohttp.ClientSession() as session, aiofiles.open(links_file, 'r') as lf:
        total_lines = sum(1 for _ in await lf.readlines())
        await lf.seek(0)
        async for line in tqdm(lf, total=total_lines, desc="Scraping Articles", unit="link"):
            link = line.strip()
            date_published, article_content = await scrape_article(session, link)
            if date_published and article_content:
                articles.append([date_published, article_content])
                print(f"URL: {link}\nDate: {date_published}\nArticle:\n{article_content}\n{'='*80}\n")
            # Save progress every batch_size articles
            if len(articles) >= batch_size:
                await save_to_csv(articles)
                articles.clear()
        # Save any remaining articles
        if articles:
            await save_to_csv(articles)

# Function to save articles to CSV asynchronously
async def save_to_csv(articles):
    df = pd.DataFrame(articles, columns=['date_published', 'article_content'])
    if not os.path.isfile(output_csv):
        df.to_csv(output_csv, index=False)
    else:
        df.to_csv(output_csv, mode='a', header=False, index=False)
    print(f"Progress saved to {output_csv}")

# Run the scraper
if __name__ == "__main__":
    asyncio.run(scrape_articles_from_links())
    print(f"Articles have been saved to {output_csv}")
