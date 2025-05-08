print("Testing Flask installation...")
try:
    from flask import Flask
    print("Flask imported successfully!")
    app = Flask(__name__)
    print("Flask app created successfully!")
    print("\nFlask is working correctly!")
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
