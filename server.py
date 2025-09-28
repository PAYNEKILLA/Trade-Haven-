import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')

PI_API_KEY = os.getenv("PI_API_KEY")
PI_API_BASE = "https://api.minepi.com"

def pi_headers():
    return {"Authorization": f"Key {PI_API_KEY}"}

@app.route("/")
def home():
    # Serve the HTML UI
    return render_template("index.html")

@app.route("/api/pi/approve", methods=["POST"])
def approve_payment():
    data = request.get_json() or {}
    payment_id = data.get("paymentId")
    if not payment_id:
        return jsonify({"error": "Missing paymentId"}), 400
    res = requests.post(f"{PI_API_BASE}/v2/payments/{payment_id}/approve",
                        headers=pi_headers())
    return jsonify(res.json()), res.status_code

@app.route("/api/pi/complete", methods=["POST"])
def complete_payment():
    data = request.get_json() or {}
    payment_id = data.get("paymentId")
    txid = data.get("txid")
    if not payment_id or not txid:
        return jsonify({"error": "Missing paymentId or txid"}), 400
    res = requests.post(f"{PI_API_BASE}/v2/payments/{payment_id}/complete",
                        headers=pi_headers(), json={"txid": txid})
    return jsonify(res.json()), res.status_code

# Domain validation (you already had this)
@app.route("/validation-key.txt")
def serve_validation_file():
    return "69ff105bb1c0488b4ef96ab43a4ec31b7938ea884dd23e39a2447ecc62f13d2cfe777b68c9ad2e45a58c8fd0d29e7e3eb5285cf9348e1a0eb7e5ff96957c1d1d\n", 200, {'Content-Type': 'text/plain'}

# Extra well-known path some validators use
@app.route("/.well-known/pi-platform/validation-key.txt")
def redirect_to_validation():
    return serve_validation_file()
