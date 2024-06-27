import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from tqdm import tqdm

# Download VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

# Load the CSV file
file_path = '/kaggle/input/scraped-articles-csv/scraped_articles.csv' #This was done on kaggle. to speed p filtering.
df = pd.read_csv(file_path)

# Fill missing values with an empty string
df['heading'].fillna('', inplace=True)
df['article_content'].fillna('', inplace=True)

# Function to preprocess text
def preprocess_text(text):
    # Convert to string if it's not already
    text = str(text)
    # Remove unwanted characters and convert to lowercase
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'\n', ' ', text)   
    text = text.lower()  # Convert to lowercase
    return text

# Apply preprocessing to the article content with a progress bar
tqdm.pandas(desc="Preprocessing")
df['article_content'] = df['article_content'].progress_apply(preprocess_text)

# Initialize the VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Function to get sentiment scores
def get_sentiment(text):
    return sid.polarity_scores(text)

# Apply sentiment analysis to the article content with a progress bar
tqdm.pandas(desc="Sentiment Analysis")
df['sentiment'] = df['article_content'].progress_apply(get_sentiment)

# Keywords for categorization
keywords = {
    'business': ['business', 'company', 'market', 'trade', 'commerce', 'industry', 'corporation', 'enterprise', 'firm', 'startup', 'venture'],
    'government': ['government', 'policy', 'regulation', 'law', 'administration', 'governance', 'authority', 'bureaucracy', 'legislation', 'public sector'],
    'stocks': ['stock', 'market', 'investment', 'shares', 'trading', 'equity', 'securities', 'portfolio', 'capital', 'dividend'],
    'fortune_500': ['Walmart', 'Amazon', 'Apple', 'CVS Health', 'UnitedHealth Group', 'Berkshire Hathaway', 'McKesson', 'AmerisourceBergen', 'Alphabet', 'ExxonMobil', 'AT&T', 'Costco', 'Cigna', 'Cardinal Health', 'Microsoft', 'Walgreens', 'Kroger', 'Home Depot', 'JPMorgan Chase', 'Verizon', 'Ford', 'General Motors', 'Anthem', 'Centene', 'Fannie Mae', 'Comcast', 'Chevron', 'Dell Technologies', 'State Farm', 'Johnson & Johnson', 'IBM', 'Target', 'Freddie Mac', 'Lowe’s', 'Marathon Petroleum', 'Procter & Gamble', 'MetLife', 'UPS', 'Boeing', 'Intel', 'Humana', 'Facebook', 'Disney', 'Pfizer', 'Goldman Sachs', 'Caterpillar', 'Lockheed Martin', 'PepsiCo', 'Bank of America', 'Merck', 'United Technologies', 'Charter Communications', 'Cisco Systems', 'HCA Healthcare', 'Nationwide', 'American Express', 'Nike', 'Best Buy', 'General Electric', 'Oracle', 'Morgan Stanley', 'Honeywell', 'Abbott Laboratories', 'Raytheon', 'Aetna', 'Bristol-Myers Squibb', 'AbbVie', 'Deere & Co.', 'Eli Lilly', 'Hewlett Packard Enterprise', 'Publix Super Markets', 'Starbucks', 'New York Life Insurance', 'Coca-Cola', 'Capital One', '3M', 'Wells Fargo', 'Allstate', 'Aflac', 'Chubb', 'Travelers', 'Prudential Financial', 'Progressive', 'Liberty Mutual', 'Guardian Life', 'Lincoln National', 'Pacific Life', 'Massachusetts Mutual', 'Northwestern Mutual', 'AIG', 'General Dynamics', 'Molina Healthcare', 'C.H. Robinson', 'Stryker', 'Cummins', 'Becton Dickinson', 'Sherwin-Williams', 'Roper Technologies', 'Parker-Hannifin', 'Rockwell Automation', 'Fortive', 'Motorola Solutions', 'Textron', 'Sensata Technologies', 'Teledyne Technologies', 'Crane Co.', 'Roper Technologies', 'Stanley Black & Decker', 'IHS Markit', 'Terex', 'Gardner Denver', 'AMETEK', 'Danaher', 'Ingersoll Rand', 'Eaton', 'Allegion', 'Fidelity National Information Services', 'Fiserv', 'Western Union', 'PayPal', 'Discover Financial Services', 'Square', 'Visa', 'Mastercard', 'Global Payments', 'American Express', 'Moody’s', 'S&P Global', 'Broadridge Financial Solutions', 'Intercontinental Exchange', 'MSCI', 'FactSet Research Systems', 'Tradeweb Markets', 'Envestnet', 'Virtu Financial', 'MarketAxess Holdings', 'Cboe Global Markets', 'Nasdaq', 'Morningstar', 'BGC Partners', 'CME Group', 'UBS', 'Barclays', 'Credit Suisse', 'Deutsche Bank', 'BNP Paribas', 'Societe Generale', 'Lazard', 'Jefferies Financial Group', 'Goldman Sachs', 'Morgan Stanley', 'JP Morgan Chase', 'Citigroup', 'Bank of America', 'Wells Fargo', 'Royal Bank of Canada', 'TD Bank', 'Scotiabank', 'Bank of Montreal', 'National Bank of Canada'],
    'natural_disasters': ['earthquake', 'flood', 'hurricane', 'disaster', 'tsunami', 'tornado', 'wildfire', 'storm', 'drought', 'landslide', 'volcano', 'avalanche', 'cyclone', 'typhoon', 'heatwave', 'blizzard', 'hailstorm'],
    'technology': ['technology', 'tech', 'innovation', 'software', 'hardware', 'gadget', 'AI', 'artificial intelligence', 'robotics', 'blockchain', 'cybersecurity'],
    'health': ['health', 'medicine', 'medical', 'doctor', 'nurse', 'hospital', 'clinic', 'disease', 'virus', 'pandemic', 'covid', 'vaccine', 'wellness', 'mental health', 'nutrition', 'fitness'],
    'environment': ['environment', 'climate', 'pollution', 'conservation', 'sustainability', 'eco-friendly', 'biodiversity', 'recycling', 'renewable energy', 'carbon footprint', 'global warming']
}

# Function to categorize articles based on sentiment and keywords
def categorize_article(row):
    heading = row['heading'].lower()
    content = row['article_content'].lower()
    sentiment = row['sentiment']
    
    # Check if the sentiment compound score meets the 99% certainty threshold
    if abs(sentiment['compound']) < 0.99:
        return 'other'
    
    for category, words in keywords.items():
        if any(word in heading or word in content for word in words):
            return category
    
    return 'other'

# Apply categorization to the dataframe with a progress bar
tqdm.pandas(desc="Categorizing")
df['category'] = df.progress_apply(categorize_article, axis=1)

# Save the dataframe to a new CSV file
output_file_path = '/kaggle/working/processed_articles_with_certainty6.csv'
df.to_csv(output_file_path, index=False)

# Print the first few rows of the dataframe to check results
print(df.head())

# Print the count of each category
category_counts = df['category'].value_counts()
print(category_counts)

# Print how many articles meet the criteria and how many do not
total_meet_criteria = category_counts.sum() - category_counts['other']
total_do_not_meet_criteria = category_counts['other']
print(f"Total articles that meet the criteria: {total_meet_criteria}")
print(f"Total articles that do not meet the criteria: {total_do_not_meet_criteria}")