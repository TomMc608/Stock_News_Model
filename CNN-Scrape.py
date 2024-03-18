import requests
from bs4 import BeautifulSoup

def scrape_cnn_article():
    url = 'https://edition.cnn.com/2024/03/18/politics/trump-464-million-dollar-bond/index.html'
    url2 = 'https://edition.cnn.com/2024/03/18/politics/supreme-court-new-york-nra/index.html'
    url3 = 'https://edition.cnn.com/2024/03/18/investing/nar-realtor-commissions-settlement-explained/index.html?iid=cnn_buildContentRecirc_end_recirc'
    url4 = 'https://edition.cnn.com/interactive/2023/11/world/climate-gender-inequality-cnnphotos-as-equals-intl-cmd/'
    try:
        response = requests.get(url3)
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

            # Save the formatted article text to a file
            save_article_to_file(formatted_article)
            print("Article saved to 'cnn_article.txt'")
        else:
            print("Article container not found on the page.")

    except requests.exceptions.RequestException as e:
        print("Error fetching the page:", e)

def format_article(article_text):
    # Remove excess newlines and whitespace
    formatted_text = '\n'.join(line.strip() for line in article_text.split('\n') if line.strip())
    return formatted_text

def save_article_to_file(article_text):
    with open('cnn_article.txt', 'w', encoding='utf-8') as file:
        file.write(article_text)

if __name__ == '__main__':
    scrape_cnn_article()
