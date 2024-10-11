from flask import Flask, request, jsonify, send_from_directory
from g4f.client import Client
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
client = Client()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(f"static/{path}"):
        return send_from_directory('static', path)
    else:
        return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['message']
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}],
        )
        return jsonify({"response": response.choices[0].message.content})
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
