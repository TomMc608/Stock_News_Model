from selenium import webdriver
from selenium.webdriver.common.by import By

def find_links_in_section(url):
    # Initialize Chrome webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Open the URL
        driver.get(url)

        # Find the specified section containing links
        section = driver.find_element(By.CSS_SELECTOR, 'body > div.pg-no-rail.pg-wrapper.pg.t-light > div > div:nth-child(2) > section')

        # Find all anchor links within the section and its descendants
        links = find_links_recursive(section)

        # Remove duplicates from the list of links
        unique_links = list(set(links))

        print("Total unique links found:", len(unique_links))
        for link in unique_links:
            print(link.get_attribute('href'))

        # Save all unique links to a text file
        save_links_to_file(unique_links, 'cnn_links_from_main_Index.txt')

    finally:
        # Close the webdriver
        driver.quit()

def find_links_recursive(element):
    # Initialize an empty list to store links
    links = []

    # Find all anchor links within the element
    anchor_links = element.find_elements(By.TAG_NAME, 'a')
    for anchor_link in anchor_links:
        links.append(anchor_link)

    # Recursively search through child elements and count their links as well
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
    start_url = "https://edition.cnn.com/sitemap.html"
    find_links_in_section(start_url)
