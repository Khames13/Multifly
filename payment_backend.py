from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulate a simple user database with payment status
users = {
    "user123": {"is_premium": False}
}

@app.route('/start_payment', methods=['POST'])
def start_payment():
    data = request.json
    user_id = data.get("user_id")
    payment_method = data.get("payment_method")  # 'paypal' or 'mpesa'

    # Simulate creating a payment order
    order_id = "ORDER123"

    return jsonify({"order_id": order_id, "message": f"Payment started with {payment_method} for user {user_id}"}), 200

@app.route('/payment_status', methods=['POST'])
def payment_status():
    data = request.json
    user_id = data.get("user_id")
    order_id = data.get("order_id")

    # Simulate checking payment status
    payment_success = True

    if payment_success:
        users[user_id]["is_premium"] = True
        return jsonify({"status": "success", "message": "Payment successful, user upgraded to premium."}), 200
    else:
        return jsonify({"status": "pending", "message": "Payment pending or failed."}), 200

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    user_id = data.get("user_id")
    transaction_code = data.get("transaction_code")
    payment_method = data.get("payment_method")

    # Simulate verification logic
    if not user_id or not transaction_code:
        return jsonify({"status": "error", "message": "Missing user ID or transaction code"}), 400

    if user_id not in users:
        users[user_id] = {"is_premium": False}

    # Simulate successful validation
    users[user_id]["is_premium"] = True

    return jsonify({"status": "success", "message": f"User {user_id} upgraded to premium with {payment_method}."}), 200

if __name__ == '__main__':
    app.run(debug=True)
