from flask import Flask, request, jsonify, render_template
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from newspaper import Article
import os

# Download required NLTK data
nltk.download('punkt', quiet=True)

app = Flask(__name__)

def get_article_info(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        return {
            'title': article.title,
            'text': article.text,
            'authors': article.authors,
            'publish_date': str(article.publish_date) if article.publish_date else None,
            'top_image': article.top_image
        }
    except Exception as e:
        return {'error': str(e)}

def generate_summary(text, num_sentences=3):
    """Generate a simple summary by extracting the first few sentences"""
    try:
        sentences = sent_tokenize(text)
        return ' '.join(sentences[:num_sentences])
    except Exception as e:
        return f"Error generating summary: {str(e)}"

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
    
    # Prepare response
    response = {
        'title': article_info['title'],
        'summary': summary,
        'authors': article_info['authors'],
        'publish_date': article_info['publish_date'],
        'image': article_info['top_image']
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
