from flask import Flask, request, jsonify, render_template
from newspaper import Article
import nltk
from nltk.tokenize import sent_tokenize
import requests
from datetime import datetime
import os
from flask_cors import CORS
from translate import Translator as LangTranslator

# Download required NLTK data
nltk.download('punkt', quiet=True)

app = Flask(__name__)
CORS(app)

def translate_text(text, target_lang):
    """Translate text to the specified language"""
    try:
        translator = LangTranslator(to_lang=target_lang)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        return f"Error translating text: {str(e)}"

def generate_summary(text, num_sentences=3):
    """Generate a summary by extracting key sentences"""
    try:
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # Simple heuristic: take the first few sentences as summary
        # In a real application, you might want to implement more sophisticated
        # summarization techniques or use a different library
        summary = ' '.join(sentences[:num_sentences])
        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def get_article_info(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        return {
            'title': article.title,
            'authors': article.authors,
            'publish_date': article.publish_date,
            'text': article.text,
            'top_image': article.top_image,
            'videos': article.movies
        }
    except Exception as e:
        return {'error': str(e)}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Get article information
    article_info = get_article_info(url)
    if 'error' in article_info:
        return jsonify({'error': article_info['error']}), 400
    
    # Generate summary
    summary = generate_summary(article_info['text'])
    
    # Get language preference from request
    lang = data.get('language', 'en')  # Default to English if no language specified
    
    # Translate summary if language is not English
    if lang != 'en':
        summary = translate_text(summary, lang)
    
    response = {
        'title': article_info['title'],
        'authors': article_info['authors'],
        'publish_date': article_info['publish_date'].isoformat() if article_info['publish_date'] else None,
        'summary': summary,
        'image': article_info['top_image']
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
