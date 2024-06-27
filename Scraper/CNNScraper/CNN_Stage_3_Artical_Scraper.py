from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import re

def scrape_links_from_urls(input_file_path, output_file_name):
    # Initialize Chrome webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Open the input file containing URLs
        with open(input_file_path, 'r') as file:
            urls = file.readlines()

        # Initialize a set to store all unique links
        all_links = set()

        # Iterate through each URL
        for url in urls:
            # Strip to remove leading/trailing whitespaces
            url = url.strip()
            if not url.startswith("http"):
                print(f"Skipping invalid URL: {url}")
                continue

            try:
                # Open the URL
                driver.get(url)
                time.sleep(2)  # Wait for page to load
            except WebDriverException as e:
                print(f"Error accessing URL: {url}")
                print(e)
                continue

            # Find all links in the page source using regular expressions
            links = find_links_in_page_source(driver.page_source)

            # Add the links to the set of all links
            all_links.update(links)

        # Save links to a text file
        save_links_to_file(all_links, output_file_name)

    finally:
        # Close the webdriver
        driver.quit()

# Find all links in the page source using regular expressions
def find_links_in_page_source(page_source):
    links = set()
    # Regular expression to match URLs
    url_pattern = r'https?://[^\s/$.?#].[^\s]*'
    # Find all matches of the URL pattern in the page source
    urls = re.findall(url_pattern, page_source)
    for url in urls:
        links.add(url)
    return links

# Save all links to a file
def save_links_to_file(links, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')

if __name__ == "__main__":
    input_file_path = "output_article_links.txt"
    output_file_name = "all_links.txt"
    scrape_links_from_urls(input_file_path, output_file_name)
