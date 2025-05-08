print("Testing imports...")
try:
    print("Importing Flask...")
    from flask import Flask
    print("Flask imported successfully")
    
    print("Importing NLTK...")
    import nltk
    print("NLTK imported successfully")
    
    print("Importing Newspaper...")
    from newspaper import Article
    print("Newspaper imported successfully")
    
    print("All imports successful!")
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
