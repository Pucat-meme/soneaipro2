from flask import Flask, request, jsonify, send_from_directory
from g4f.client import Client
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = Client()

@app.route('/')
def index():
    return send_from_directory('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(path)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['message']
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}],
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    if not os.path.exists('index.html'):
        os.makedirs('static')
    app.run(debug=True)
