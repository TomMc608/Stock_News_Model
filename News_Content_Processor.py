import pandas as pd
from textblob import TextBlob
from dateutil import parser
import pytz
# Assuming your CSV file has columns: 'date', 'heading', 'article_content'
df = pd.read_csv('your_file.csv')


def convert_date(date_str):
    # Parse the date string to datetime
    dt = parser.parse(date_str)
    # Convert to a common timezone, e.g., UTC
    dt_utc = dt.astimezone(pytz.utc)
    return dt_utc

df['date'] = df['date'].apply(convert_date)


def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

df['sentiment'] = df['article_content'].apply(analyze_sentiment)
df.to_csv('processed_file.csv', index=False)
