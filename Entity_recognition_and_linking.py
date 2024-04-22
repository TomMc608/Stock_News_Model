import pandas as pd
import spacy
from tqdm import tqdm
import time

# Load the English NLP model
nlp = spacy.load('en_core_web_sm')

# Function to extract entities from text
def extract_entities(text):
    # Create a SpaCy document that includes the detected entities
    doc = nlp(text)
    # Extract entities and their labels
    return [(ent.text, ent.label_) for ent in doc.ents]

def main():
    # Load data from CSV file
    data = pd.read_csv('processed_output.csv')

    # Fill NaN values with empty strings to avoid type errors in NLP processing
    data['article_content'] = data['article_content'].fillna('')

    # Initialize tqdm to display a progress bar
    tqdm.pandas(desc="Extracting entities")

    # Start time for ETA calculation
    start_time = time.time()

    # Apply the extract_entities function to each row in the article_content column with progress bar
    data['entities'] = data['article_content'].progress_apply(extract_entities)

    # Calculate and print the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    # Save the results back to a new CSV file
    data.to_csv('annotated_news_articles.csv', index=False)
    print("Entities have been extracted and the results are saved in 'annotated_news_articles.csv'.")


if __name__ == "__main__":
    main()
