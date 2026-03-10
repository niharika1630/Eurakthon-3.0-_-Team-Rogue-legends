from flask import Flask, render_template, jsonify
import random
from datetime import datetime
from engine import evaluate_transaction

app = Flask(__name__)

locations = ["Bangalore", "Mumbai", "Delhi", "Dubai", "London"]

stats = {
    "total": 0,
    "flagged": 0,
    "blocked": 0
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate")
def generate():

    txn = {
        "sender": "User_001",
        "receiver": f"User_{random.randint(100,200)}",
        "amount": random.randint(100,150000),
        "known_receiver": random.choice([True, False]),
        "location": random.choice(locations),
        "last_location": random.choice(locations),
        "hour": datetime.now().hour,
        "oldbalanceOrg": random.randint(50000,200000),
        "newbalanceOrig": random.randint(10000,150000),
        "oldbalanceDest": random.randint(20000,300000),
        "newbalanceDest": random.randint(30000,400000),
        "step": random.randint(1,743)
    }

    result = evaluate_transaction(txn)

    stats["total"] += 1
    if result["risk"] == "Medium":
        stats["flagged"] += 1
    if result["risk"] == "High":
        stats["blocked"] += 1

    result["transaction"] = txn
    result["stats"] = stats

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
