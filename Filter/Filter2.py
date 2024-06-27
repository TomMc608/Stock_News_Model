import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tqdm import tqdm
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import math
from multiprocessing import Pool, cpu_count
import tkinter as tk
from tkinter import filedialog, messagebox
import time

# Define the filter_articles function at the top level
keywords = {
    'business': ['business', 'company', 'market', 'trade', 'commerce', 'industry', 'corporation', 'enterprise', 'firm', 'startup', 'venture'],
    'government': ['government', 'policy', 'regulation', 'law', 'administration', 'governance', 'authority', 'bureaucracy', 'legislation', 'public sector'],
    'stocks': ['stock', 'market', 'investment', 'shares', 'trading', 'equity', 'securities', 'portfolio', 'capital', 'dividend'],
    'fortune_500': ['Walmart', 'Amazon', 'Apple', 'CVS Health', 'UnitedHealth Group', 'Berkshire Hathaway', 'McKesson', 'AmerisourceBergen', 'Alphabet', 'ExxonMobil', 'AT&T', 'Costco', 'Cigna', 'Cardinal Health', 'Microsoft', 'Walgreens', 'Kroger', 'Home Depot', 'JPMorgan Chase', 'Verizon', 'Ford', 'General Motors', 'Anthem', 'Centene', 'Fannie Mae', 'Comcast', 'Chevron', 'Dell Technologies', 'State Farm', 'Johnson & Johnson', 'IBM', 'Target', 'Freddie Mac', 'Lowe’s', 'Marathon Petroleum', 'Procter & Gamble', 'MetLife', 'UPS', 'Boeing', 'Intel', 'Humana', 'Facebook', 'Disney', 'Pfizer', 'Goldman Sachs', 'Caterpillar', 'Lockheed Martin', 'PepsiCo', 'Bank of America', 'Merck', 'United Technologies', 'Charter Communications', 'Cisco Systems', 'HCA Healthcare', 'Nationwide', 'American Express', 'Nike', 'Best Buy', 'General Electric', 'Oracle', 'Morgan Stanley', 'Honeywell', 'Abbott Laboratories', 'Raytheon', 'Aetna', 'Bristol-Myers Squibb', 'AbbVie', 'Deere & Co.', 'Eli Lilly', 'Hewlett Packard Enterprise', 'Publix Super Markets', 'Starbucks', 'New York Life Insurance', 'Coca-Cola', 'Capital One', '3M', 'Wells Fargo', 'Allstate', 'Aflac', 'Chubb', 'Travelers', 'Prudential Financial', 'Progressive', 'Liberty Mutual', 'Guardian Life', 'Lincoln National', 'Pacific Life', 'Massachusetts Mutual', 'Northwestern Mutual', 'AIG', 'General Dynamics', 'Molina Healthcare', 'C.H. Robinson', 'Stryker', 'Cummins', 'Becton Dickinson', 'Sherwin-Williams', 'Roper Technologies', 'Parker-Hannifin', 'Rockwell Automation', 'Fortive', 'Motorola Solutions', 'Textron', 'Sensata Technologies', 'Teledyne Technologies', 'Crane Co.', 'Roper Technologies', 'Stanley Black & Decker', 'IHS Markit', 'Terex', 'Gardner Denver', 'AMETEK', 'Danaher', 'Ingersoll Rand', 'Eaton', 'Allegion', 'Fidelity National Information Services', 'Fiserv', 'Western Union', 'PayPal', 'Discover Financial Services', 'Square', 'Visa', 'Mastercard', 'Global Payments', 'American Express', 'Moody’s', 'S&P Global', 'Broadridge Financial Solutions', 'Intercontinental Exchange', 'MSCI', 'FactSet Research Systems', 'Tradeweb Markets', 'Envestnet', 'Virtu Financial', 'MarketAxess Holdings', 'Cboe Global Markets', 'Nasdaq', 'Morningstar', 'BGC Partners', 'CME Group', 'UBS', 'Barclays', 'Credit Suisse', 'Deutsche Bank', 'BNP Paribas', 'Societe Generale', 'Lazard', 'Jefferies Financial Group', 'Goldman Sachs', 'Morgan Stanley', 'JP Morgan Chase', 'Citigroup', 'Bank of America', 'Wells Fargo', 'Royal Bank of Canada', 'TD Bank', 'Scotiabank', 'Bank of Montreal', 'National Bank of Canada'],
    'natural_disasters': ['earthquake', 'flood', 'hurricane', 'disaster', 'tsunami', 'tornado', 'wildfire', 'storm', 'drought', 'landslide', 'volcano', 'avalanche', 'cyclone', 'typhoon', 'heatwave', 'blizzard', 'hailstorm']
}

def keyword_filter(text, keywords):
    match_count = 0
    total_keywords = sum(len(words) for words in keywords.values())
    for category, words in keywords.items():
        for word in words:
            if word in text:
                match_count += 1
    match_percentage = (match_count / total_keywords) * 100 if total_keywords > 0 else 0
    return match_percentage

def filter_articles(row):
    match_percentage = keyword_filter(row['processed_text'], keywords)
    row['match_percentage'] = match_percentage
    row['is_relevant'] = match_percentage > 0
    return row

def process_chunk(chunk):
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

    chunk['text'] = chunk['text'].fillna('')  # Fill NaN values with empty string
    chunk['tokens'] = chunk['text'].apply(word_tokenize)
    stop_words = set(stopwords.words('english'))
    chunk['filtered_tokens'] = chunk['tokens'].apply(lambda tokens: [word for word in tokens if word.lower() not in stop_words])
    chunk['lemmatized_tokens'] = chunk['filtered_tokens'].apply(lambda tokens: [token.lemma_ for token in nlp(' '.join(tokens))])
    chunk['processed_text'] = chunk['lemmatized_tokens'].apply(lambda tokens: ' '.join(tokens))

    chunk = chunk.apply(filter_articles, axis=1)
    return chunk

def main():
    # Configuration
    testing_mode = True  # Set to True for testing mode, False for full run
    test_rows = 100  # Number of rows to process in testing mode
    cpu_usage = 0.9  # Proportion of CPU to use (0.9 for 90%)
    chunksize = 10000  # Define chunk size

    # Function to select CSV files
    def select_files():
        file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
        return list(file_paths)

    # Initialize tkinter root
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Select CSV files
    file_paths = select_files()
    if len(file_paths) != 2:
        messagebox.showerror("Error", "Please select exactly two CSV files.")
        return

    # Calculate the total number of rows
    total_rows = 0
    for file_path in file_paths:
        total_rows += pd.read_csv(file_path, usecols=[0]).shape[0]

    if testing_mode:
        total_chunks = math.ceil(test_rows / chunksize)
    else:
        total_chunks = math.ceil(total_rows / chunksize)

    num_cpus = math.ceil(cpu_count() * cpu_usage)
    first_chunk = True  # Initialize first_chunk

    start_time = time.time()  # Record the start time

    # Create a tqdm progress bar with ETA countdown
    pbar = tqdm(total=total_chunks, desc="Processing", dynamic_ncols=True, unit="chunk", leave=True, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]")

    for file_path in file_paths:
        for chunk in pd.read_csv(file_path, chunksize=chunksize):
            # Combine heading and content if heading exists
            if 'heading' in chunk.columns:
                chunk['text'] = chunk['heading'] + ' ' + chunk['article_content']
            else:
                chunk['text'] = chunk['article_content']

            # Handle the date column
            if 'date_published' in chunk.columns:
                chunk['date'] = chunk['date_published']
            elif 'date' not in chunk.columns:
                chunk['date'] = pd.NaT  # Assign missing date as NaT if neither column exists

            if testing_mode:
                chunk = chunk.head(test_rows)

            with Pool(num_cpus) as pool:
                processed_chunks = pool.map(process_chunk, [chunk])
                processed_chunk = pd.concat(processed_chunks)

            # Write chunk to CSV
            processed_chunk.to_csv('filtered_articles.csv', mode='a', header=first_chunk, index=False)
            first_chunk = False

            # Update the progress bar
            pbar.update(1)

            # Calculate the estimated time remaining
            elapsed_time = time.time() - start_time
            eta = elapsed_time / pbar.n * (total_chunks - pbar.n)
            pbar.set_postfix({'ETA': f"{eta:.0f} seconds"})

    pbar.close()
    print(f"\nFiltered data saved to filtered_articles.csv")

if __name__ == "__main__":
    main()