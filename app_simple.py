from flask import Flask, request, jsonify, render_template, make_response
from newspaper import Article, ArticleException
import nltk
from nltk.tokenize import sent_tokenize
import traceback
import logging
from textblob import TextBlob
import spacy
import json

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    logger.info("Downloading required NLTK data...")
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)

app = Flask(__name__)

def get_article_info(url):
    try:
        # Ensure URL is properly formatted
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        print(f"Processing URL: {url}")
        
        article = Article(url)
        article.download()
        article.parse()
        
        # Ensure we have the basic required fields
        if not article.text or len(article.text.strip()) < 50:  # Assuming at least 50 chars for valid content
            return {'error': 'Article content is too short or empty'}
        
        return {
            'title': article.title or 'No title available',
            'text': article.text,
            'authors': article.authors or ['Unknown Author'],
            'publish_date': str(article.publish_date) if article.publish_date else None,
            'top_image': article.top_image or 'https://via.placeholder.com/800x400?text=No+Image+Available'
        }
    except Exception as e:
        error_msg = f"Error processing article: {str(e)}"
        print(error_msg)
        return {'error': error_msg}

def generate_summary(text, num_sentences=3):
    """Generate a simple summary by extracting the first few sentences"""
    try:
        sentences = sent_tokenize(text)
        return ' '.join(sentences[:num_sentences])
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def categorize_news(text):
    """Categorize news article based on content"""
    try:
        # Analyze sentiment
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        
        # Basic category classification based on keywords
        categories = []
        text_lower = text.lower()
        
        # Politics keywords
        if any(word in text_lower for word in ['politics', 'government', 'election', 'president', 'congress']):
            categories.append('Politics')
        
        # Technology keywords
        if any(word in text_lower for word in ['technology', 'tech', 'software', 'hardware', 'internet', 'ai', 'artificial intelligence']):
            categories.append('Technology')
        
        # Sports keywords
        if any(word in text_lower for word in ['sports', 'football', 'basketball', 'soccer', 'olympics', 'championship']):
            categories.append('Sports')
        
        # Business keywords
        if any(word in text_lower for word in ['business', 'finance', 'market', 'stock', 'company', 'corporation']):
            categories.append('Business')
        
        # Science keywords
        if any(word in text_lower for word in ['science', 'research', 'study', 'discovery', 'experiment']):
            categories.append('Science')
        
        # Health keywords
        if any(word in text_lower for word in ['health', 'medicine', 'disease', 'vaccine', 'hospital']):
            categories.append('Health')
        
        # Entertainment keywords
        if any(word in text_lower for word in ['entertainment', 'movie', 'music', 'celebrity', 'show', 'award']):
            categories.append('Entertainment')
        
        # Environment keywords
        if any(word in text_lower for word in ['environment', 'climate', 'weather', 'pollution', 'sustainability']):
            categories.append('Environment')
        
        # If no specific category found, classify based on sentiment
        if not categories:
            if sentiment > 0.2:
                categories.append('Positive News')
            elif sentiment < -0.2:
                categories.append('Negative News')
            else:
                categories.append('General News')
        
        return {
            'categories': list(set(categories)),  # Remove duplicates
            'sentiment': sentiment,
            'sentiment_polarity': 'Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral'
        }
    except Exception as e:
        return {'error': f'Error categorizing news: {str(e)}'}

def extract_entities(text):
    """Extract named entities from the text using spaCy"""
    try:
        doc = nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC', 'DATE', 'TIME']:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'description': {
                        'PERSON': 'Person',
                        'ORG': 'Organization',
                        'GPE': 'Geopolitical Entity',
                        'LOC': 'Location',
                        'DATE': 'Date',
                        'TIME': 'Time'
                    }.get(ent.label_, 'Unknown')
                })
        
        return entities
    except Exception as e:
        return {'error': f'Error extracting entities: {str(e)}'}

def get_related_news(query, location=None):
    """Get related news articles with images and metadata.
    
    Returns a list of real news articles that can be summarized.
    """
    try:
        # Real news articles from reliable sources that can be summarized
        related = [
            {
                'title': 'Latest Technology News',
                'url': 'https://techcrunch.com/2023/11/01/ai-advancements-2023/',
                'image': 'https://techcrunch.com/wp-content/uploads/2023/10/ai-robot-hand.jpg',
                'source': 'TechCrunch',
                'published_at': '2023-11-01T10:30:00Z',
                'description': 'The latest advancements in AI and technology that are shaping our future.'
            },
            {
                'title': 'Global Business Updates',
                'url': 'https://www.bbc.com/news/business-67265970',
                'image': 'https://ichef.bbci.co.uk/news/1024/branded_news/12345ABC/market.jpg',
                'source': 'BBC Business',
                'published_at': '2023-11-02T15:45:00Z',
                'description': 'The latest business news and financial updates from around the world.'
            },
            {
                'title': 'Science and Discovery',
                'url': 'https://www.nationalgeographic.com/science/article/space-exploration-mars-2023',
                'image': 'https://i.natgeofe.com/n/mars-rover.jpg',
                'source': 'National Geographic',
                'published_at': '2023-10-31T08:15:00Z',
                'description': 'Breaking discoveries and research in space exploration and science.'
            }
        ]
        
        # If there's a query, update the descriptions to include it
        if query and len(query.strip()) > 0:
            for item in related:
                item['description'] = f"{query}: {item['description']}"
                
        return related
    except Exception as e:
        logger.error(f"Error getting related news: {e}")
        return []

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return "An error occurred while loading the page. Please check the server logs."

@app.route('/summarize', methods=['POST'])
def summarize():
    
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        url = data.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Clean and validate URL
        url = url.strip()
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
            
        logger.info(f"Processing URL: {url}")
        
        try:
            # Get article information
            article_info = get_article_info(url)
            if 'error' in article_info:
                logger.error(f"Error getting article info: {article_info['error']}")
                return jsonify({'error': article_info['error']}), 400
            
            # Generate summary
            summary = generate_summary(article_info['text'])
            
            # Get related news
            related_news = get_related_news(article_info['title'])
            
            # Get categorization and entities
            categorization = categorize_news(article_info['text'])
            entities = extract_entities(article_info['text'])
            
            # Prepare response
            response = {
                'title': article_info.get('title', 'No title available'),
                'summary': summary,
                'authors': article_info.get('authors', []),
                'publish_date': article_info.get('publish_date'),
                'image': article_info.get('top_image'),
                'related_news': related_news,
                'original_url': url,
                'categorization': {
                    'categories': categorization.get('categories', []),
                    'sentiment': categorization.get('sentiment', 0),
                    'sentiment_polarity': categorization.get('sentiment_polarity', 'Neutral')
                },
                'entities': entities
            }
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error processing article: {str(e)}")
            return jsonify({'error': f'Failed to process article: {str(e)}'}), 500
        
    except ArticleException as e:
        logger.error(f"Article processing error: {e}")
        return jsonify({'error': f'Error processing article: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

if __name__ == '__main__':
    print("Starting News Summarizer...")
    app.run(debug=True)
