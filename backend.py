import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# Load trained model
model = joblib.load("model.pkl")

def calculate_rule_score(txn):
    score = 0
    reasons = []

    if txn["amount"] > 50000:
        score += 40
        reasons.append("High transaction amount")

    if not txn["known_receiver"]:
        score += 25
        reasons.append("New receiver detected")

    if txn["location"] != txn["last_location"]:
        score += 30
        reasons.append("Location changed suddenly")

    if txn["hour"] < 6:
        score += 15
        reasons.append("Unusual transaction time")

    return score, reasons


def calculate_ml_score(txn):
    features = np.array([[txn["amount"], txn["hour"]]])
    anomaly = model.decision_function(features)[0]
    ml_score = int((1 - anomaly) * 50)
    return max(0, ml_score)


def evaluate_transaction(txn):
    rule_score, reasons = calculate_rule_score(txn)
    ml_score = calculate_ml_score(txn)

    total_score = rule_score + ml_score

    if total_score < 40:
        status = "Low"
    elif total_score < 70:
        status = "Medium"
    else:
        status = "High"

    return total_score, status, reasons