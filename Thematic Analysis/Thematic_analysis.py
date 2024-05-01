import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from tqdm import tqdm

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def load_data(filepath):
    """Load data from a CSV file into a DataFrame."""
    return pd.read_csv(filepath)

def preprocess_text(text):
    """Tokenize, lemmatize, and remove stopwords from the text."""
    # Check if text is not a string (possibly NaN or None), then return an empty list
    if not isinstance(text, str):
        return []

    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    return [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and word.isalpha()]


def perform_thematic_analysis(data, num_topics=50):
    """Perform thematic analysis using TF-IDF and NMF for topic modeling."""
    tqdm.pandas(desc="Preprocessing text")
    processed_data = data['article_content'].progress_apply(preprocess_text)
    
    tfidf_vectorizer = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False, stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(processed_data)
    
    nmf = NMF(n_components=num_topics, random_state=42)
    W = nmf.fit_transform(tfidf_matrix)
    H = nmf.components_
    
    data['theme'] = W.argmax(axis=1)
    return data, H, tfidf_vectorizer.get_feature_names_out()  # Updated to use get_feature_names_out


def save_results(data, filepath):
    """Save the thematic analysis results to a new CSV file."""
    data.to_csv(filepath, index=False)

# Example usage
if __name__ == "__main__":
    data = load_data('./Event Extraction/Events.csv')
    analyzed_data, _, _ = perform_thematic_analysis(data)
    save_results(analyzed_data, 'thematic_analysis_results.csv')
