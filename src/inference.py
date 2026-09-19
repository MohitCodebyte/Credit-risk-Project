# ============================================================
# CREDIT RISK INFERENCE MODULE
# ============================================================

from pathlib import Path

import joblib
import numpy as np
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "credit_risk_model.pkl"
THRESHOLD_PATH = BASE_DIR / "models" / "credit_risk_threshold.pkl"
RISK_CONFIG_PATH = BASE_DIR / "models" / "risk_scoring_config.pkl"


# ============================================================
# 2. LOAD MODEL ARTIFACTS
# ============================================================

model = joblib.load(MODEL_PATH)
threshold = joblib.load(THRESHOLD_PATH)
risk_config = joblib.load(RISK_CONFIG_PATH)


# ============================================================
# 3. MODEL FEATURE SCHEMA
# ============================================================

NUMERICAL_FEATURES = [
    "age",
    "employment_length_years",
    "annual_income",
    "credit_score",
    "loan_amount",
    "loan_term_months",
    "interest_rate",
    "existing_debt",
    "existing_loans",
    "previous_delinquencies",
    "previous_defaults",
    "credit_history_years",
    "open_credit_accounts",
    "dependents",
    "monthly_income",
    "monthly_emi",
    "debt_to_income_ratio",
    "loan_to_income_ratio",
    "bank_gross_npa_ratio",
    "emi_to_income_ratio",
    "total_debt_exposure",
    "credit_history_age_ratio",
    "has_previous_delinquency",
]

CATEGORICAL_FEATURES = [
    "bank",
    "employment_type",
    "home_ownership",
    "loan_purpose",
]

MODEL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES


# ============================================================
# 4. RBI BANK NPA BENCHMARK
# ============================================================

BANK_NPA_RATIOS = {
    "BANK OF BARODA": 2.26214992742974,
    "BANK OF INDIA": 3.26536678896202,
    "BANK OF MAHARASHTRA": 1.74473831218546,
    "CANARA BANK": 2.93758462729564,
    "CENTRAL BANK OF INDIA": 3.17984343335963,
    "INDIAN BANK": 3.0909050201749,
    "INDIAN OVERSEAS BANK": 2.13892621416291,
    "PUNJAB AND SIND BANK": 3.3834240860415,
    "PUNJAB NATIONAL BANK": 3.9477105374595,
    "STATE BANK OF INDIA": 1.82150230896745,
    "UCO BANK": 2.6904304939544,
    "UNION BANK OF INDIA": 3.59655817766716,
    "AXIS BANK LIMITED": 1.32826199953408,
    "BANDHAN BANK LIMITED": 4.70676522194868,
    "CITY UNION BANK LIMITED": 3.08701971587577,
    "DCB BANK LIMITED": 2.9865586320811,
    "FEDERAL BANK LTD": 1.83742290329885,
    "HDFC BANK LTD.": 1.33138574025635,
    "ICICI BANK LIMITED": 1.72990720227469,
    "NAINITAL BANK LTD": 7.78417717559281,
}


# ============================================================
# 5. FEATURE ENGINEERING FOR NEW BORROWER
# ============================================================

def prepare_features(data):
    """
    Prepare raw borrower input for the trained model.
    """

    df = pd.DataFrame([data])

    # --------------------------------------------------------
    # Bank NPA benchmark
    # --------------------------------------------------------

    if "bank_gross_npa_ratio" not in df.columns:

        bank = df["bank"].iloc[0]

        if bank not in BANK_NPA_RATIOS:
            raise ValueError(
                f"Unsupported bank: {bank}"
            )

        df["bank_gross_npa_ratio"] = BANK_NPA_RATIOS[bank]

    # --------------------------------------------------------
    # Derived features
    # --------------------------------------------------------

    df["emi_to_income_ratio"] = (
        df["monthly_emi"] /
        df["monthly_income"]
    )

    df["emi_to_income_ratio"] = (
        df["emi_to_income_ratio"]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
        .clip(0, 3)
    )

    df["total_debt_exposure"] = (
        df["existing_debt"] +
        df["loan_amount"]
    )

    df["credit_history_age_ratio"] = (
        df["credit_history_years"] /
        df["age"]
    )

    df["credit_history_age_ratio"] = (
        df["credit_history_age_ratio"]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0)
        .clip(0, 1)
    )

    df["has_previous_delinquency"] = (
        df["previous_delinquencies"] > 0
    ).astype(int)

    # --------------------------------------------------------
    # Keep exact model feature order
    # --------------------------------------------------------

    missing_features = [
        feature
        for feature in MODEL_FEATURES
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing model features: {missing_features}"
        )

    return df[MODEL_FEATURES]


# ============================================================
# 6. RISK SCORE
# ============================================================

def calculate_risk_score(default_probability):
    """
    Convert predicted default probability
    into a 0-100 project risk score.
    """

    probability = float(default_probability)

    probability = np.clip(
        probability,
        0,
        1
    )

    return float(round(
        probability * 100,
        2
    ))


# ============================================================
# 7. RISK CATEGORY
# ============================================================

def get_risk_category(risk_score):

    if risk_score < 25:
        return "Low Risk"

    elif risk_score < 50:
        return "Medium Risk"

    elif risk_score < 75:
        return "High Risk"

    else:
        return "Very High Risk"


# ============================================================
# 8. MAIN PREDICTION FUNCTION
# ============================================================

def predict_credit_risk(data):
    """
    Complete credit risk prediction pipeline.

    Returns:
        default_probability
        risk_score
        risk_category
        default_prediction
    """

    # Prepare features
    features = prepare_features(data)

    # Predict probability
    default_probability = float(
        model.predict_proba(features)[0, 1]
    )

    # Risk score
    risk_score = calculate_risk_score(
        default_probability
    )

    # Risk category
    risk_category = get_risk_category(
        risk_score
    )

    # Default classification
    default_prediction = int(
        default_probability >= float(threshold)
    )

    return {
        "default_probability": round(
            default_probability * 100,
            2
        ),

        "risk_score": risk_score,

        "risk_category": risk_category,

        "default_prediction": default_prediction,

        "default_label": (
            "Potential Default"
            if default_prediction == 1
            else "Lower Default Risk"
        )
    }


# ============================================================
# 9. MODULE STATUS
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("CREDIT RISK INFERENCE MODULE")
    print("=" * 70)

    print(f"✓ Model loaded: {MODEL_PATH.name}")
    print(f"✓ Threshold loaded: {THRESHOLD_PATH.name}")
    print(f"✓ Risk configuration loaded: {RISK_CONFIG_PATH.name}")

    print("\n✓ Inference module ready.")