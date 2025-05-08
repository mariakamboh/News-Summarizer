from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World! This is a minimal Flask app."

if __name__ == '__main__':
    print("Starting minimal Flask app...")
    app.run(debug=True)
