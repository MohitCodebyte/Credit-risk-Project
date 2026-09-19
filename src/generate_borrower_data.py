import os
import numpy as np
import pandas as pd
from faker import Faker

# ============================================================
# 1. Configuration
# ============================================================

RANDOM_SEED = 42
N_BORROWERS = 10000

np.random.seed(RANDOM_SEED)

fake = Faker("en_IN")
Faker.seed(RANDOM_SEED)

RBI_FILE = "data/processed/bank_risk_benchmark.csv"
OUTPUT_FILE = "data/synthetic/borrower_credit_data.csv"

# ============================================================
# 2. Load RBI bank-level benchmark data
# ============================================================

print("=" * 60)
print("LOADING RBI BANK RISK BENCHMARK")
print("=" * 60)

rbi_df = pd.read_csv(RBI_FILE)

print("\nRBI Dataset Shape:", rbi_df.shape)

# ============================================================
# 3. Remove aggregate bank-group rows
# ============================================================

aggregate_rows = [
    "PUBLIC SECTOR BANKS",
    "PRIVATE SECTOR BANKS",
    "FOREIGN BANKS",
    "SMALL FINANCE BANKS",
    "ALL SCHEDULED COMMERCIAL BANKS"
]

bank_df = rbi_df[
    ~rbi_df["banks"].isin(aggregate_rows)
].copy()

bank_df = bank_df.reset_index(drop=True)

print("Individual Banks Available:", len(bank_df))

# ============================================================
# 4. Select representative banks
# ============================================================

selected_banks = [
    "BANK OF BARODA",
    "BANK OF INDIA",
    "BANK OF MAHARASHTRA",
    "CANARA BANK",
    "CENTRAL BANK OF INDIA",
    "INDIAN BANK",
    "INDIAN OVERSEAS BANK",
    "PUNJAB AND SIND BANK",
    "PUNJAB NATIONAL BANK",
    "STATE BANK OF INDIA",
    "UCO BANK",
    "UNION BANK OF INDIA",
    "AXIS BANK LIMITED",
    "BANDHAN BANK LIMITED",
    "CITY UNION BANK LIMITED",
    "DCB BANK LIMITED",
    "FEDERAL BANK LTD",
    "HDFC BANK LTD.",
    "ICICI BANK LIMITED",
    "NAINITAL BANK LTD"
]

bank_df = bank_df[
    bank_df["banks"].isin(selected_banks)
].copy()

bank_df = bank_df.reset_index(drop=True)

print("\nSelected Banks:")

for bank in bank_df["banks"]:
    print("-", bank)

print("\nNumber of Selected Banks:", len(bank_df))

# ============================================================
# 5. Validate selected banks
# ============================================================

if len(bank_df) != len(selected_banks):

    missing_banks = sorted(
        set(selected_banks) - set(bank_df["banks"])
    )

    raise ValueError(
        "\nSome selected banks were not found in RBI dataset:\n"
        + "\n".join(missing_banks)
    )

# ============================================================
# 6. Bank borrower distribution
# ============================================================

bank_weights = {
    "STATE BANK OF INDIA": 0.16,
    "HDFC BANK LTD.": 0.12,
    "ICICI BANK LIMITED": 0.11,
    "AXIS BANK LIMITED": 0.09,
    "BANK OF BARODA": 0.07,
    "CANARA BANK": 0.07,
    "PUNJAB NATIONAL BANK": 0.06,
    "UNION BANK OF INDIA": 0.05,
    "BANK OF INDIA": 0.04,
    "INDIAN BANK": 0.04,
    "BANK OF MAHARASHTRA": 0.03,
    "CENTRAL BANK OF INDIA": 0.03,
    "INDIAN OVERSEAS BANK": 0.025,
    "UCO BANK": 0.025,
    "PUNJAB AND SIND BANK": 0.015,
    "BANDHAN BANK LIMITED": 0.025,
    "FEDERAL BANK LTD": 0.02,
    "CITY UNION BANK LIMITED": 0.015,
    "DCB BANK LIMITED": 0.015,
    "NAINITAL BANK LTD": 0.02
}

weights = np.array(
    [bank_weights[bank] for bank in bank_df["banks"]]
)

weights = weights / weights.sum()

# ============================================================
# 7. Generate borrower IDs
# ============================================================

borrower_ids = [
    f"BRW{str(i).zfill(6)}"
    for i in range(1, N_BORROWERS + 1)
]

# ============================================================
# 8. Assign banks to borrowers
# ============================================================

borrower_banks = np.random.choice(
    bank_df["banks"].values,
    size=N_BORROWERS,
    p=weights
)

borrowers = pd.DataFrame({
    "borrower_id": borrower_ids,
    "bank": borrower_banks
})

# ============================================================
# 9. Age
# ============================================================

borrowers["age"] = np.random.randint(
    21,
    61,
    size=N_BORROWERS
)

# ============================================================
# 10. Employment type
# ============================================================

borrowers["employment_type"] = np.random.choice(
    [
        "Salaried",
        "Self-Employed",
        "Business Owner",
        "Contract"
    ],
    size=N_BORROWERS,
    p=[
        0.55,
        0.20,
        0.15,
        0.10
    ]
)

# ============================================================
# 11. Employment length
# ============================================================

borrowers["employment_length_years"] = np.clip(
    np.random.gamma(
        shape=2.5,
        scale=3.0,
        size=N_BORROWERS
    ),
    0.5,
    30
).round(1)

# ============================================================
# 12. Annual income
# ============================================================

income = np.random.lognormal(
    mean=np.log(600000),
    sigma=0.55,
    size=N_BORROWERS
)

borrowers["annual_income"] = np.clip(
    income,
    180000,
    5000000
).round(0)

# ============================================================
# 13. Credit score
# ============================================================

borrowers["credit_score"] = np.clip(
    np.random.normal(
        loc=710,
        scale=70,
        size=N_BORROWERS
    ),
    300,
    900
).round(0).astype(int)

# ============================================================
# 14. Loan amount
# ============================================================

borrowers["loan_amount"] = np.clip(
    np.random.lognormal(
        mean=np.log(700000),
        sigma=0.70,
        size=N_BORROWERS
    ),
    50000,
    5000000
).round(0)

# ============================================================
# 15. Loan term
# ============================================================

borrowers["loan_term_months"] = np.random.choice(
    [
        12,
        24,
        36,
        48,
        60,
        84,
        120
    ],
    size=N_BORROWERS,
    p=[
        0.05,
        0.08,
        0.18,
        0.12,
        0.30,
        0.12,
        0.15
    ]
)

# ============================================================
# 16. Interest rate
# ============================================================

borrowers["interest_rate"] = np.clip(
    np.random.normal(
        loc=11.5,
        scale=2.5,
        size=N_BORROWERS
    ),
    6,
    20
).round(2)

# ============================================================
# 17. Existing debt
# ============================================================

borrowers["existing_debt"] = np.clip(
    borrowers["annual_income"]
    * np.random.uniform(
        0.05,
        1.5,
        size=N_BORROWERS
    ),
    0,
    6000000
).round(0)

# ============================================================
# 18. Existing loans
# ============================================================

borrowers["existing_loans"] = np.random.poisson(
    lam=1.5,
    size=N_BORROWERS
)

borrowers["existing_loans"] = np.clip(
    borrowers["existing_loans"],
    0,
    8
)

# ============================================================
# 19. Previous delinquencies
# ============================================================

borrowers["previous_delinquencies"] = np.random.poisson(
    lam=0.35,
    size=N_BORROWERS
)

borrowers["previous_delinquencies"] = np.clip(
    borrowers["previous_delinquencies"],
    0,
    6
)

# ============================================================
# 20. Previous defaults
# ============================================================

borrowers["previous_defaults"] = np.random.binomial(
    n=1,
    p=0.08,
    size=N_BORROWERS
)

# ============================================================
# 21. Credit history
# ============================================================

borrowers["credit_history_years"] = np.clip(
    (
        borrowers["age"]
        - np.random.randint(
            18,
            25,
            size=N_BORROWERS
        )
    ),
    1,
    40
)

# ============================================================
# 22. Open credit accounts
# ============================================================

borrowers["open_credit_accounts"] = np.clip(
    np.random.poisson(
        lam=3.5,
        size=N_BORROWERS
    ),
    1,
    15
)

# ============================================================
# 23. Dependents
# ============================================================

borrowers["dependents"] = np.random.choice(
    [0, 1, 2, 3, 4, 5],
    size=N_BORROWERS,
    p=[
        0.20,
        0.20,
        0.30,
        0.18,
        0.08,
        0.04
    ]
)

# ============================================================
# 24. Home ownership
# ============================================================

borrowers["home_ownership"] = np.random.choice(
    [
        "Own",
        "Mortgage",
        "Rent"
    ],
    size=N_BORROWERS,
    p=[
        0.35,
        0.30,
        0.35
    ]
)

# ============================================================
# 25. Loan purpose
# ============================================================

borrowers["loan_purpose"] = np.random.choice(
    [
        "Home",
        "Personal",
        "Education",
        "Medical",
        "Business",
        "Vehicle"
    ],
    size=N_BORROWERS,
    p=[
        0.20,
        0.25,
        0.10,
        0.08,
        0.17,
        0.20
    ]
)

# ============================================================
# 26. Monthly income
# ============================================================

borrowers["monthly_income"] = (
    borrowers["annual_income"] / 12
).round(2)

# ============================================================
# 27. Monthly EMI
# ============================================================

monthly_rate = (
    borrowers["interest_rate"] / 100 / 12
)

months = borrowers["loan_term_months"]

borrowers["monthly_emi"] = (
    borrowers["loan_amount"]
    * monthly_rate
    * (1 + monthly_rate) ** months
    / (
        (1 + monthly_rate) ** months - 1
    )
).round(2)

# ============================================================
# 28. Debt-to-income ratio
# ============================================================

borrowers["debt_to_income_ratio"] = (
    (
        borrowers["existing_debt"] / 12
        + borrowers["monthly_emi"]
    )
    / borrowers["monthly_income"]
)

borrowers["debt_to_income_ratio"] = np.clip(
    borrowers["debt_to_income_ratio"],
    0.01,
    2.50
).round(4)

# ============================================================
# 29. Loan-to-income ratio
# ============================================================

borrowers["loan_to_income_ratio"] = (
    borrowers["loan_amount"]
    / borrowers["annual_income"]
)

borrowers["loan_to_income_ratio"] = np.clip(
    borrowers["loan_to_income_ratio"],
    0.01,
    15
).round(4)

# ============================================================
# 30. Merge RBI bank-level risk data
# ============================================================

bank_risk = bank_df[
    [
        "banks",
        "gross_npas",
        "gross_advances",
        "gross_npas_to_gross_advances_ratio_percent"
    ]
].copy()

bank_risk = bank_risk.rename(
    columns={
        "banks": "bank",
        "gross_npas": "bank_gross_npas",
        "gross_advances": "bank_gross_advances",
        "gross_npas_to_gross_advances_ratio_percent":
            "bank_gross_npa_ratio"
    }
)

borrowers = borrowers.merge(
    bank_risk,
    on="bank",
    how="left"
)

# ============================================================
# 31. Validate RBI mapping
# ============================================================

missing_bank_risk = borrowers[
    "bank_gross_npa_ratio"
].isna().sum()

if missing_bank_risk > 0:

    raise ValueError(
        f"{missing_bank_risk} borrowers could not be "
        f"mapped to RBI bank risk data."
    )

# ============================================================
# 32. Create borrower risk score
# ============================================================

risk_score = (

    -4.0

    # Lower credit score = higher risk
    + (700 - borrowers["credit_score"]) * 0.010

    # Higher debt burden = higher risk
    + borrowers["debt_to_income_ratio"] * 1.20

    # Higher loan burden = higher risk
    + borrowers["loan_to_income_ratio"] * 0.12

    # Previous delinquencies = higher risk
    + borrowers["previous_delinquencies"] * 0.45

    # Previous default = strong risk signal
    + borrowers["previous_defaults"] * 1.10

    # Bank-level NPA risk
    + borrowers["bank_gross_npa_ratio"] * 0.07

    # Higher interest rate = slightly higher risk
    + (borrowers["interest_rate"] - 10) * 0.06

    # Longer employment = slightly lower risk
    - borrowers["employment_length_years"] * 0.018
)

# ============================================================
# 33. Convert risk score into probability
# ============================================================

raw_probability = 1 / (
    1 + np.exp(-risk_score)
)

# ============================================================
# 34. Create relative risk percentile
# ============================================================

risk_percentile = risk_score.rank(
    pct=True
)

# ============================================================
# 35. Create default probability
# ============================================================

default_probability = (
    0.015
    + risk_percentile * 0.32
)

# Previous defaults
default_probability += (
    borrowers["previous_defaults"] * 0.035
)

# Previous delinquencies
default_probability += (
    borrowers["previous_delinquencies"] * 0.012
)

# Strong credit score reduces risk
default_probability -= np.where(
    borrowers["credit_score"] >= 760,
    0.035,
    0
)

# Very low credit score increases risk
default_probability += np.where(
    borrowers["credit_score"] < 580,
    0.045,
    0
)

# Keep probabilities within sensible boundaries
default_probability = np.clip(
    default_probability,
    0.005,
    0.70
)

# ============================================================
# 36. Generate initial default flags
# ============================================================

random_values = np.random.random(
    size=N_BORROWERS
)

borrowers["default_flag"] = (
    random_values < default_probability
).astype(int)

# ============================================================
# 37. Calibrate final default rate
# ============================================================

# Target default rate for synthetic borrower dataset
# 10,000 borrowers -> exactly 700 defaults
target_default_rate = 0.07

target_defaults = int(
    N_BORROWERS * target_default_rate
)

current_defaults = int(
    borrowers["default_flag"].sum()
)

# ------------------------------------------------------------
# If defaults are below target
# Select highest-risk non-default borrowers
# ------------------------------------------------------------

if current_defaults < target_defaults:

    required = target_defaults - current_defaults

    candidates = borrowers[
        borrowers["default_flag"] == 0
    ]

    candidate_scores = default_probability[
        candidates.index
    ]

    selected_indices = (
        candidate_scores
        .nlargest(required)
        .index
    )

    borrowers.loc[
        selected_indices,
        "default_flag"
    ] = 1

# ------------------------------------------------------------
# If defaults are above target
# Remove defaults from lowest-risk borrowers
# ------------------------------------------------------------

elif current_defaults > target_defaults:

    required = current_defaults - target_defaults

    candidates = borrowers[
        borrowers["default_flag"] == 1
    ]

    candidate_scores = default_probability[
        candidates.index
    ]

    selected_indices = (
        candidate_scores
        .nsmallest(required)
        .index
    )

    borrowers.loc[
        selected_indices,
        "default_flag"
    ] = 0


# ============================================================
# 38. Create project-defined risk categories
# ============================================================

# Risk tiers are based on relative borrower risk percentile.
# These are project-defined categories, NOT official RBI categories.

borrowers["risk_category"] = pd.cut(
    risk_percentile,
    bins=[
        -np.inf,
        0.50,
        0.80,
        0.95,
        np.inf
    ],
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ],
    include_lowest=True
)

# ============================================================
# 39. Remove internal variables
# ============================================================

# These were only used during synthetic target generation.
# They must not become ML features.

del raw_probability
del risk_score
del risk_percentile
del default_probability

# ============================================================
# 40. Round numerical columns
# ============================================================

round_columns = [
    "annual_income",
    "loan_amount",
    "existing_debt",
    "monthly_income",
    "monthly_emi",
    "debt_to_income_ratio",
    "loan_to_income_ratio",
    "bank_gross_npas",
    "bank_gross_advances",
    "bank_gross_npa_ratio"
]

for column in round_columns:

    borrowers[column] = borrowers[
        column
    ].round(2)

# ============================================================
# 41. Final column order
# ============================================================

final_columns = [
    "borrower_id",
    "bank",
    "age",
    "employment_type",
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
    "home_ownership",
    "loan_purpose",
    "monthly_income",
    "monthly_emi",
    "debt_to_income_ratio",
    "loan_to_income_ratio",
    "bank_gross_npas",
    "bank_gross_advances",
    "bank_gross_npa_ratio",
    "risk_category",
    "default_flag"
]

borrowers = borrowers[
    final_columns
]

# ============================================================
# 42. Final validation
# ============================================================

print("\n" + "=" * 60)
print("FINAL BORROWER DATA VALIDATION")
print("=" * 60)

print("\nDataset Shape:")
print(borrowers.shape)

print("\nColumns:")
print(borrowers.columns.tolist())

print("\nMissing Values:")
print(borrowers.isnull().sum())

print("\nDuplicate Rows:")
print(borrowers.duplicated().sum())

print("\nUnique Borrowers:")
print(borrowers["borrower_id"].nunique())

# ============================================================
# 43. Default distribution
# ============================================================

print("\nDefault Distribution:")
print(
    borrowers["default_flag"]
    .value_counts()
    .sort_index()
)

print("\nDefault Percentage:")

default_percentage = (
    borrowers["default_flag"].mean() * 100
)

print(
    round(default_percentage, 2),
    "%"
)

# ============================================================
# 44. Risk category distribution
# ============================================================

print("\nRisk Category Distribution:")
print(
    borrowers["risk_category"]
    .value_counts()
)

# ============================================================
# 45. Bank distribution
# ============================================================

print("\nBank Distribution:")
print(
    borrowers["bank"]
    .value_counts()
)

# ============================================================
# 46. Default rate by risk category
# ============================================================

print("\nDefault Rate by Risk Category:")

risk_default_rate = (
    borrowers
    .groupby(
        "risk_category",
        observed=False
    )["default_flag"]
    .mean()
    .mul(100)
    .round(2)
)

print(risk_default_rate)

# ============================================================
# 47. Default rate by bank
# ============================================================

print("\nDefault Rate by Bank:")

bank_default_rate = (
    borrowers
    .groupby("bank")["default_flag"]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
    .round(2)
)

print(bank_default_rate)

# ============================================================
# 48. Sample records
# ============================================================

print("\nSample Borrower Records:")

print(
    borrowers
    .head(10)
    .to_string(index=False)
)

# ============================================================
# 49. Create output directory
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

# ============================================================
# 50. Save dataset
# ============================================================

borrowers.to_csv(
    OUTPUT_FILE,
    index=False
)

# ============================================================
# 51. Completion message
# ============================================================

print("\n" + "=" * 60)
print("BORROWER DATA GENERATION COMPLETED")
print("=" * 60)

print("\nSaved File:")
print(OUTPUT_FILE)

print("\nFinal Dataset Shape:")
print(borrowers.shape)

print("\nFinal Default Rate:")
print(
    round(
        borrowers["default_flag"].mean() * 100,
        2
    ),
    "%"
)