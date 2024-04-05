import pandas as pd
from transformers import pipeline
from dateutil import parser
import pytz

# Initialize the sentiment analysis pipeline with BERT
# This example uses the `bert-base-cased` model for sentiment analysis.
# You can choose a model more suited to your needs from Hugging Face's model hub.
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to load the CSV file
def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

# Function to convert dates to UTC
from dateutil import tz

# A dictionary mapping known timezone abbreviations to their full names
TZ_INFOS = {
    'EDT': tz.gettz('America/New_York'),  # Eastern Daylight Time
    'EST': tz.gettz('America/New_York'),  # Eastern Standard Time
    # Add any other timezones you need to handle
}

def convert_date(date_str):
    try:
        # Ensure the input is a string
        if not isinstance(date_str, str):
            print(f"Non-string date encountered: {date_str}. Skipping...")
            return None

        # Strip known prefixes and any leading/trailing whitespace
        date_str = date_str.replace("Published", "").replace("Updated", "").strip()
        
        dt = parser.parse(date_str, tzinfos=TZ_INFOS)
        dt_utc = dt.astimezone(pytz.utc)
        return dt_utc
    except ValueError as e:
        print(f"Error parsing date: {date_str}. Error: {e}. Skipping...")
        return None



# BERT-based sentiment analysis function
from transformers import AutoTokenizer

# Initialize the tokenizer for your model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment_bert(text):
    # Ensure the input is a string
    if not isinstance(text, str):
        print("Non-string input received in sentiment analysis. Skipping...")
        return None, None

    try:
        inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)
        outputs = sentiment_pipeline.model(**inputs)
        scores = outputs[0][0].detach().numpy()
        label = 'POSITIVE' if scores.argmax() == 1 else 'NEGATIVE'
        score = scores.max()
        return label, score
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return None, None




# Main function to process the CSV file
def process_csv(input_file, output_file):
    df = load_csv(input_file)
    if df is not None:
        df['date'] = df['date'].apply(convert_date)
        # Apply BERT-based sentiment analysis
        df[['sentiment', 'score']] = df['article_content'].apply(
            lambda x: pd.Series(analyze_sentiment_bert(x))
        )
        try:
            df.to_csv(output_file, index=False)
            print(f"Processed file saved to {output_file}")
        except Exception as e:
            print(f"Error saving processed file: {e}")

# Example usage
if __name__ == "__main__":
    process_csv('scraped_articles.csv', 'processed_file_with_bert.csv')
