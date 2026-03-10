import joblib
import numpy as np

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")


def evaluate_transaction(txn):

    # ---------- RULE ENGINE ----------
    rule_score = 0
    reasons = []

    if txn["amount"] > 100000:
        rule_score += 40
        reasons.append("High transaction amount")

    if not txn["known_receiver"]:
        rule_score += 25
        reasons.append("New receiver detected")

    if txn["location"] != txn["last_location"]:
        rule_score += 30
        reasons.append("Location changed suddenly")

    if txn["hour"] < 6:
        rule_score += 15
        reasons.append("Unusual transaction time")

    # ---------- ML ENGINE ----------
    features = np.array([[
        txn["amount"],
        txn["oldbalanceOrg"],
        txn["newbalanceOrig"],
        txn["oldbalanceDest"],
        txn["newbalanceDest"],
        txn["step"]
    ]])

    scaled = scaler.transform(features)
    anomaly_score = model.decision_function(scaled)[0]
    ml_score = int((1 - anomaly_score) * 50)

    total_score = rule_score + ml_score

    if total_score < 40:
        risk = "Low"
    elif total_score < 70:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "risk_score": total_score,
        "risk": risk,
        "reasons": reasons,
        "rule_score": rule_score,
        "ml_score": ml_score
    }