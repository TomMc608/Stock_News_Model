import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

# Define the base URL and years/months to scrape
base_url = "https://www.nbcnews.com/archive/articles/{year}/{month}"
years = range(2003, 2025)
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

# Directory to save the links
output_file = "nbc_news_links.txt"

# Function to scrape links for a given year and month
def scrape_links(year, month):
    url = base_url.format(year=year, month=month)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find('main', class_='MonthPage')
        if main_content:
            links = main_content.find_all('a', href=True)
            return [link['href'] for link in links]
    return []

# Main function to scrape links for all specified years and months
def scrape_all_links():
    total_links = 0
    missing_links = []
    with open(output_file, 'w') as f, tqdm(total=len(years) * len(months), desc="Scraping", unit="task") as pbar:
        for year in years:
            for month in months:
                links = scrape_links(year, month)
                if links:
                    for link in links:
                        f.write(f"{link}\n")
                    total_links += len(links)
                else:
                    missing_links.append(f"{month} {year}")
                pbar.update(1)
    return total_links, missing_links

# Run the scraper
if __name__ == "__main__":
    total_links, missing_links = scrape_all_links()
    print(f"Total number of links found: {total_links}")
    if missing_links:
        print("Missing links for the following months and years:")
        for entry in missing_links:
            print(entry)
    else:
        print("No missing links.")

    print(f"Links have been saved to {output_file}")
