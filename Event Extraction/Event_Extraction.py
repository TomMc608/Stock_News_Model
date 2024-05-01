import os
import stanza
from stanza.server import CoreNLPClient
import pandas as pd
from tqdm import tqdm

# Set the environment variable for CoreNLP
corenlp_path = 'C:/Users/mcivtj1/Desktop/Stock_News_Model/corenlp'
os.environ['CORENLP_HOME'] = corenlp_path

# Function to ensure CoreNLP is installed and start the server
def start_corenlp_server():
    # Install CoreNLP if it's not already installed
    if not os.path.exists(corenlp_path):
        print("CoreNLP not found, installing...")
        stanza.install_corenlp(dir=corenlp_path)

    # Start the CoreNLP client
    client = CoreNLPClient(
        annotators=['tokenize', 'ssplit', 'pos', 'lemma', 'ner'],
        memory='15G',
        threads=6,
        be_quiet=True,
        timeout=30000
    )
    client.start()
    return client

# Function to extract entities with NER
def extract_entities(text, client):
    ann = client.annotate(text)
    entities = []
    for sentence in ann.sentence:
        for token in sentence.token:
            entities.append((token.word, token.ner))
    return entities

def main():
    # Start the CoreNLP server
    client = start_corenlp_server()

    # Load the data
    data = pd.read_csv('./Enitiy Recognition And Linking/Enitiy_Recognition_And_Linking.csv')
    data['article_content'] = data['article_content'].fillna('')

    # Initialize tqdm for progress display
    tqdm.pandas(desc="Extracting entities")

    # Apply the entity extraction function
    data['Events'] = data['article_content'].progress_apply(lambda x: extract_entities(x, client))

    # Stop the CoreNLP client
    client.stop()

    # Save the results to a new CSV
    data.to_csv('Events.csv', index=False)
    print("Entities have been extracted and the results are saved in 'Events.csv'.")

if __name__ == "__main__":
    main()
