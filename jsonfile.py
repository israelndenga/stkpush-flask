from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():
    data = request.get_json()
    
    # Save to a file
    with open("mpesa_callback.json", "a") as f:
        json.dump(data, f, indent=4)
        f.write("\n\n")

    print("✅ Callback received and saved.")
    return jsonify({"ResultCode": 0, "ResultDesc": "Callback received successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
