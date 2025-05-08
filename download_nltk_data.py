import nltk
import os

def download_nltk_data():
    print("Downloading NLTK data...")
    try:
        # Download the punkt tokenizer data
        print("Downloading punkt tokenizer data...")
        nltk.download('punkt', quiet=True)
        
        # Download the punkt_tab data
        print("Downloading punkt_tab data...")
        nltk.download('punkt_tab', quiet=True)
        
        # Download the stopwords data (in case it's needed later)
        print("Downloading stopwords data...")
        nltk.download('stopwords', quiet=True)
        
        print("\nNLTK data downloaded successfully!")
        
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
        print("\nPlease try running this script with administrator privileges.")

if __name__ == "__main__":
    download_nltk_data()
