import pandas as pd
from transformers import pipeline
import os
from tqdm import tqdm

# Initialize the sentiment analysis pipeline
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)

def perform_sentiment_analysis(text):
    """Perform sentiment analysis with proper truncation."""
    if pd.isna(text) or not isinstance(text, str):
        return "No Text", None  # Ensure only strings are processed
    
    try:
        result = sentiment_pipeline(text, truncation=True, max_length=512)
        label = result[0]['label']
        score = result[0]['score']
        return label, score
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Error", None

def process_csv(input_filepath):
    df = pd.read_csv(input_filepath)
    
    # Initialize tqdm to display a progress bar
    tqdm.pandas(desc="Analyzing Sentiment")

    # Apply sentiment analysis with progress bar
    sentiments = df['article_content'].progress_apply(lambda x: perform_sentiment_analysis(x) if pd.notnull(x) else (None, None))

    # Split sentiments into separate columns
    df['sentiment_label'], df['sentiment_score'] = zip(*sentiments)

    # Save the processed DataFrame to a new CSV file
    output_filepath = os.path.join(os.getcwd(), 'Semtiment_Analysis.csv')  # Save in the current working directory
    df.to_csv(output_filepath, index=False)
    print(f"Processed data saved to {output_filepath}")

if __name__ == "__main__":
    input_csv_path = 'scraped_articles.csv'  # Update this path to your input CSV file
    process_csv(input_csv_path)
