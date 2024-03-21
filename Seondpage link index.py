from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

def scrape_links_from_urls(input_file_path, output_file_name):
    # Initialize Chrome webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Open the input file containing URLs
        with open(input_file_path, 'r') as file:
            urls = file.readlines()

        # Initialize a list to store all unique links
        all_links = []

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
            except WebDriverException as e:
                print(f"Error accessing URL: {url}")
                print(e)
                continue

            # Find all anchor links on the page
            links = find_links_recursive(driver)

            # Add the links to the list of all links
            all_links.extend(links)

        # Remove duplicates from the list of links
        unique_links = list(set(all_links))

        # Filter out links containing the word "article"
        article_links = [link for link in unique_links if 'article' in link.lower()]

        print("Total unique links found:", len(article_links))
        for link in article_links:
            print(link)

        # Save article links to a text file
        save_links_to_file(article_links, output_file_name)

    finally:
        # Close the webdriver
        driver.quit()

# Recursively find all anchor links within the page using XPath
def find_links_recursive(driver):
    links = []
    anchor_links = driver.find_elements(By.XPATH, '//a')
    for anchor_link in anchor_links:
        href = anchor_link.get_attribute('href')
        if href:
            links.append(href)
    return links

# Save all links to a file
def save_links_to_file(links, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')

if __name__ == "__main__":
    input_file_path = "output_article_links.txt"  # Change this to your input file path
    output_file_name = "output_article_links_done.txt"  # Change this to your output file name
    scrape_links_from_urls(input_file_path, output_file_name)
