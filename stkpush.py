from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, your Render app is live 🚀"

from flask import Flask, request, jsonify
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# === Safaricom Credentials ===
consumer_key = "apSEeKMsRr5Amkdw8tNpk20PqT0Gw3xSsaMZvE0jLdrDJyce"
consumer_secret = "NzsxZzkX4Yr3R4LAjcKKFaxh8GRAWaAFAchCkwBzRkzkKmxGmR9NChRiKBLnhycQ"
business_short_code = "4152280"   # Your Till Number
passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"          # From Safaricom portal
callback_url = "https://your-domain.com/mpesa/callback"  # Replace with real URL later

# === Generate Access Token ===
def generate_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return response.json()["access_token"]

# === STK Push Endpoint ===
@app.route("/stkpush", methods=["POST"])
def stkpush():
    data = request.json
    phone = data.get("phone")
    amount = data.get("amount")

    access_token = generate_access_token()
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode("utf-8")

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": business_short_code,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": "Order001",
        "TransactionDesc": "Website Payment"
    }

    response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
                             json=payload, headers=headers)

    return jsonify(response.json())

# === Callback Endpoint ===
@app.route("/mpesa/callback", methods=["POST"])
def callback():
    data = request.json
    print("✅ Callback received:", data)   # For testing, logs in terminal
    return jsonify({"ResultCode": 0, "ResultDesc": "Callback received successfully"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
