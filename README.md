# AI-Powered News Summarizer

A web application that generates concise summaries of news articles from any URL and provides related news from the same region.

## Features

- Extracts and summarizes news articles from any URL
- Displays article metadata (title, author, publication date)
- Shows article images when available
- Provides related news suggestions
- Clean, responsive, and modern UI
- Fast and efficient summarization using BART model

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository or download the source code
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask development server:

```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`
3. Paste a news article URL in the input field and click "Summarize"

## How It Works

1. The application uses `newspaper3k` to extract article content from the provided URL
2. The extracted text is then processed by a pre-trained BART model to generate a concise summary
3. The summary, along with article metadata and related news, is displayed in a clean, responsive interface

## Technologies Used

- Backend: Python, Flask
- Frontend: HTML, JavaScript, Tailwind CSS
- NLP: Transformers (Hugging Face), BART model
- Web Scraping: Newspaper3k

## Note

- The first time you run the application, it will download the BART model (approximately 1.6GB)
- For production use, consider using a proper WSGI server like Gunicorn
- The related news feature currently returns placeholder data. To enable real related news, you'll need to integrate with a news API service

## License

MIT License
