from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:*", "http://127.0.0.1:*", "null"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"]
    }
})

# Ensure the data directory exists
DATA_DIR = 'card_data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/api/submit-card', methods=['POST', 'OPTIONS'])
def submit_card():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Dados não recebidos"
            }), 400
            
        # Add timestamp
        data['timestamp'] = datetime.now().isoformat()
        
        # Generate a unique filename based on timestamp
        filename = f"card_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        # Save the data
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            "success": True,
            "message": "Dados do cartão recebidos e salvos com sucesso",
            "filename": filename
        }), 200
        
    except Exception as e:
        print(f"Erro ao processar requisição: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Erro ao processar os dados: {str(e)}"
        }), 500

@app.route('/api/list-cards', methods=['GET', 'OPTIONS'])
def list_cards():
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        cards = []
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
                    card_data = json.load(f)
                    cards.append({
                        'filename': filename,
                        'data': card_data
                    })
        
        return jsonify({
            "success": True,
            "cards": cards
        }), 200
        
    except Exception as e:
        print(f"Erro ao processar requisição: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Erro ao listar cartões: {str(e)}"
        }), 500

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
