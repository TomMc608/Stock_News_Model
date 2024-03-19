from selenium import webdriver
from selenium.webdriver.common.by import By

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
            # Open the URL
            driver.get(url.strip())  # Strip to remove leading/trailing whitespaces

            # Find the specified section containing links
            section = driver.find_element(By.CSS_SELECTOR, 'body > div.pg-no-rail.pg-wrapper.pg.t-light > div > div:nth-child(2)')

            # Find all anchor links within the section and its descendants
            links = find_links_recursive(section)

            # Add the links to the list of all links
            all_links.extend(links)

        # Remove duplicates from the list of links
        unique_links = list(set(all_links))

        print("Total unique links found:", len(unique_links))
        for link in unique_links:
            print(link.get_attribute('href'))

        # Save all unique links to a text file
        save_links_to_file(unique_links, output_file_name)

    finally:
        # Close the webdriver
        driver.quit()

# Recursively find all anchor links within an element
def find_links_recursive(element):
    links = []
    anchor_links = element.find_elements(By.TAG_NAME, 'a')
    for anchor_link in anchor_links:
        links.append(anchor_link)
    child_elements = element.find_elements(By.XPATH, './/*')
    for child_element in child_elements:
        links.extend(find_links_recursive(child_element))
    return links

# Save all links to a file
def save_links_to_file(links, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link.get_attribute('href') + '\n')

if __name__ == "__main__":
    input_file_path = "cnn_links_from_main_Index.txt"
    output_file_name = "links_from_Index_page.txt"
    scrape_links_from_urls(input_file_path, output_file_name)
