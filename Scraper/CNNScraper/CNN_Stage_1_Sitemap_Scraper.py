from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

def find_links_on_page(url, output_file_name):
    # Initialize Chrome webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Open the URL
        driver.get(url)

        # Find all anchor links on the page
        links = find_links_recursive(driver)

        # Filter links to keep only those containing the word "article"
        filtered_links = [link for link in links if 'article' in link.lower()]

        print("Total unique links found:", len(filtered_links))
        for link in filtered_links:
            print(link)

        # Save filtered links to a text file
        save_links_to_file(filtered_links, output_file_name)

    except WebDriverException as e:
        print("WebDriverException occurred:", e)

    finally:
        # Close the webdriver
        driver.quit()

# Recursively find all anchor links within the page using XPath
def find_links_recursive(driver):
    links = []
    anchor_links = driver.find_elements(By.TAG_NAME, 'a')
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
    start_url = "https://edition.cnn.com/sitemap.html"
    output_file_name = "output_links_from_Main_Index.txt"  
    find_links_on_page(start_url, output_file_name)
