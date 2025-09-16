import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PI_API_KEY = os.getenv("PI_API_KEY")
PI_API_BASE = "https://api.minepi.com"

def pi_headers():
    return {"Authorization": f"Key {PI_API_KEY}"}

@app.route("/")
def home():
    return "Flask backend is running. Trade Haven ✅"

@app.route("/api/pi/approve", methods=["POST"])
def approve_payment():
    data = request.get_json()
    payment_id = data.get("paymentId")

    if not payment_id:
        return jsonify({"error": "Missing paymentId"}), 400

    res = requests.post(f"{PI_API_BASE}/v2/payments/{payment_id}/approve", headers=pi_headers())
    return jsonify(res.json()), res.status_code

@app.route("/api/pi/complete", methods=["POST"])
def complete_payment():
    data = request.get_json()
    payment_id = data.get("paymentId")
    txid = data.get("txid")

    if not payment_id or not txid:
        return jsonify({"error": "Missing paymentId or txid"}), 400

    res = requests.post(
        f"{PI_API_BASE}/v2/payments/{payment_id}/complete",
        headers=pi_headers(),
        json={"txid": txid}
    )
    return jsonify(res.json()), res.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


