from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'ok', 'message': 'Gemini proxy is running'}), 200

@app.route('/generate', methods=['POST'])
def generate():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify({'error': 'GEMINI_API_KEY not set'}), 500

    data = request.get_json() or {}
    # Если клиент передал простой prompt, обернём его в формат API Gemini
    prompt = data.get("prompt")
    if prompt:
        data = {"contents": [{"parts": [{"text": prompt}]}]}

    # Отправляем запрос к Gemini API
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    try:
        response = requests.post(
            url,
            params={"key": api_key},
            json=data,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return jsonify({'error': 'Request failed', 'details': str(e)}), 502

    # Возвращаем ответ Gemini как JSON
    try:
        result = response.json()
    except ValueError:
        return response.text, response.status_code  # на случай не-JSON ошибки

    return jsonify(result), response.status_code
