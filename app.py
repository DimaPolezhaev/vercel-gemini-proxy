from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CLOUDFLARE_URL = "https://gemini-proxy.gemini-proxy-perozhizni.workers.dev/"

@app.route("/", methods=["GET"])
def home():
    return {"status": "ok", "message": "Vercel proxy is forwarding to Cloudflare"}

@app.route("/generate", methods=["POST"])
def forward():
    try:
        response = requests.post(
            CLOUDFLARE_URL,
            headers={"Content-Type": "application/json"},
            json=request.get_json(),
            timeout=30
        )
        return response.text, response.status_code, {"Content-Type": "application/json"}
    except Exception as e:
        return jsonify({"error": str(e)}), 500
