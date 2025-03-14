from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



@app.route('/process', methods=['POST'])
def process_input():
    user_input = request.json.get('input', '')  # Get input from the frontend
    # Perform some Python logic (example: reversing the input)
    result = user_input[::-1]
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
