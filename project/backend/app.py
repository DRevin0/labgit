from flask import Flask, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app) 

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "online",
        "message": "Привет от бэкенда!",
        "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)