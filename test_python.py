print("Python is working!")
print("This is a test script.")

# Try importing required modules
try:
    import flask
    print("Flask is installed!")
except ImportError:
    print("Flask is NOT installed!")

try:
    import nltk
    print("NLTK is installed!")
except ImportError:
    print("NLTK is NOT installed!")

try:
    from newspaper import Article
    print("Newspaper3k is installed!")
except ImportError:
    print("Newspaper3k is NOT installed!")
