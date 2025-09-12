from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Simple test app", "status": "working"})

@app.route('/test')
def test():
    return jsonify({"message": "Test endpoint working"})

@app.route('/api/test')
def api_test():
    return jsonify({"message": "API test endpoint working"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
