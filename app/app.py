from flask import Flask, render_template, request
import sys
from pathlib import Path


# ============================================================
# PROJECT PATH CONFIGURATION
# ============================================================

# app/app.py
#     ↓
# parent = app/
#     ↓
# parent.parent = Credit Risk Project/

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add project root to Python path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# MODEL / INFERENCE IMPORT
# ============================================================

from src.inference import predict_credit_risk


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/")
def home():
    """
    Main landing page.

    Displays:
    - Hero section
    - Project information
    - Risk assessment form
    - Technology section
    """

    return render_template("index.html")


# ============================================================
# DASHBOARD ROUTE
# ============================================================

@app.route("/dashboard")
def dashboard():
    """
    Credit Risk Analytics Dashboard.

    Currently renders the dashboard template.
    Real dataset-driven dashboard integration can be
    connected separately.
    """

    return render_template("dashboard.html")


# ============================================================
# ABOUT ROUTE
# ============================================================

@app.route("/about")
def about():
    """
    About page for the Credit Risk Analytics System.
    """

    return render_template("about.html")


# ============================================================
# METHODOLOGY ROUTE
# ============================================================

@app.route("/methodology")
def methodology():
    """
    Displays the complete ML methodology used by
    the Credit Risk Analytics System.
    """

    return render_template("methodology.html")

@app.route("/assess-risk")
def assess_risk():
    return render_template("assess-risk.html")


# ============================================================
# CREDIT RISK PREDICTION ROUTE
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():
    """
    Receives borrower information from the assessment form,
    validates the submitted values, sends the data to the
    trained ML model and displays the prediction result.
    """

    try:

        # ----------------------------------------------------
        # READ FORM VALUES
        # ----------------------------------------------------

        data = {
            "bank": request.form["bank"].strip(),

            "age": int(request.form["age"]),

            "employment_type":
                request.form["employment_type"].strip(),

            "employment_length_years":
                float(request.form["employment_length_years"]),

            "annual_income":
                float(request.form["annual_income"]),

            "credit_score":
                float(request.form["credit_score"]),

            "loan_amount":
                float(request.form["loan_amount"]),

            "loan_term_months":
                int(request.form["loan_term_months"]),

            "interest_rate":
                float(request.form["interest_rate"]),

            "existing_debt":
                float(request.form["existing_debt"]),

            "existing_loans":
                int(request.form["existing_loans"]),

            "previous_delinquencies":
                int(request.form["previous_delinquencies"]),

            "previous_defaults":
                int(request.form["previous_defaults"]),

            "credit_history_years":
                float(request.form["credit_history_years"]),

            "open_credit_accounts":
                int(request.form["open_credit_accounts"]),

            "dependents":
                int(request.form["dependents"]),

            "home_ownership":
                request.form["home_ownership"].strip(),

            "loan_purpose":
                request.form["loan_purpose"].strip(),

            "monthly_income":
                float(request.form["monthly_income"]),

            "monthly_emi":
                float(request.form["monthly_emi"]),

            "debt_to_income_ratio":
                float(request.form["debt_to_income_ratio"]),

            "loan_to_income_ratio":
                float(request.form["loan_to_income_ratio"]),
        }


        # ====================================================
        # BACKEND VALIDATION
        # ====================================================

        validate_borrower_data(data)


        # ====================================================
        # MODEL PREDICTION
        # ====================================================

        result = predict_credit_risk(data)


        # ====================================================
        # RESULT PAGE
        # ====================================================

        return render_template(
            "result.html",
            result=result,
            data=data
        )


    # ========================================================
    # VALIDATION ERROR
    # ========================================================

    except ValueError as e:

        return render_template(
            "error.html",
            error_code=400,
            error_title="Invalid Assessment Data",
            error_message=str(e)
        ), 400


    # ========================================================
    # MISSING FORM FIELD
    # ========================================================

    except KeyError as e:

        field_name = str(e).replace("'", "")

        return render_template(
            "error.html",
            error_code=400,
            error_title="Incomplete Assessment",
            error_message=(
                f"The required field '{field_name}' "
                "was not provided. Please complete all "
                "required assessment fields."
            )
        ), 400


    # ========================================================
    # UNEXPECTED ERROR
    # ========================================================

    except Exception as e:

        print(
            "\n"
            + "=" * 70
            + "\n"
            + "PREDICTION ERROR"
            + "\n"
            + "=" * 70
            + "\n"
            + str(e)
            + "\n"
            + "=" * 70
        )

        return render_template(
            "error.html",
            error_code=500,
            error_title="Prediction Service Error",
            error_message=(
                "The credit risk assessment could not be "
                "completed right now. Please verify the "
                "submitted information and try again."
            )
        ), 500


# ============================================================
# BORROWER DATA VALIDATION
# ============================================================

def validate_borrower_data(data):
    """
    Performs backend validation before sending borrower
    information to the ML model.

    This protects the prediction endpoint from invalid
    or unrealistic form values.
    """

    # --------------------------------------------------------
    # AGE
    # --------------------------------------------------------

    age = data["age"]

    if age < 18 or age > 100:
        raise ValueError(
            "Age must be between 18 and 100 years."
        )


    # --------------------------------------------------------
    # EMPLOYMENT LENGTH
    # --------------------------------------------------------

    employment_length = data[
        "employment_length_years"
    ]

    if employment_length < 0 or employment_length > 60:
        raise ValueError(
            "Employment length must be between "
            "0 and 60 years."
        )


    # --------------------------------------------------------
    # ANNUAL INCOME
    # --------------------------------------------------------

    annual_income = data["annual_income"]

    if annual_income <= 0:
        raise ValueError(
            "Annual income must be greater than zero."
        )


    # --------------------------------------------------------
    # MONTHLY INCOME
    # --------------------------------------------------------

    monthly_income = data["monthly_income"]

    if monthly_income <= 0:
        raise ValueError(
            "Monthly income must be greater than zero."
        )


    # --------------------------------------------------------
    # CREDIT SCORE
    # --------------------------------------------------------

    credit_score = data["credit_score"]

    if credit_score < 300 or credit_score > 900:
        raise ValueError(
            "Credit score must be between 300 and 900."
        )


    # --------------------------------------------------------
    # LOAN AMOUNT
    # --------------------------------------------------------

    loan_amount = data["loan_amount"]

    if loan_amount <= 0:
        raise ValueError(
            "Loan amount must be greater than zero."
        )


    # --------------------------------------------------------
    # LOAN TERM
    # --------------------------------------------------------

    loan_term = data["loan_term_months"]

    if loan_term <= 0 or loan_term > 480:
        raise ValueError(
            "Loan term must be between 1 and 480 months."
        )


    # --------------------------------------------------------
    # INTEREST RATE
    # --------------------------------------------------------

    interest_rate = data["interest_rate"]

    if interest_rate < 0 or interest_rate > 50:
        raise ValueError(
            "Interest rate must be between 0% and 50%."
        )


    # --------------------------------------------------------
    # EXISTING DEBT
    # --------------------------------------------------------

    existing_debt = data["existing_debt"]

    if existing_debt < 0:
        raise ValueError(
            "Existing debt cannot be negative."
        )


    # --------------------------------------------------------
    # EXISTING LOANS
    # --------------------------------------------------------

    existing_loans = data["existing_loans"]

    if existing_loans < 0 or existing_loans > 100:
        raise ValueError(
            "Existing loans must be between 0 and 100."
        )


    # --------------------------------------------------------
    # PREVIOUS DELINQUENCIES
    # --------------------------------------------------------

    previous_delinquencies = data[
        "previous_delinquencies"
    ]

    if (
        previous_delinquencies < 0
        or previous_delinquencies > 100
    ):
        raise ValueError(
            "Previous delinquencies must be between "
            "0 and 100."
        )


    # --------------------------------------------------------
    # PREVIOUS DEFAULTS
    # --------------------------------------------------------

    previous_defaults = data["previous_defaults"]

    if previous_defaults < 0 or previous_defaults > 50:
        raise ValueError(
            "Previous defaults must be between 0 and 50."
        )


    # --------------------------------------------------------
    # CREDIT HISTORY
    # --------------------------------------------------------

    credit_history_years = data[
        "credit_history_years"
    ]

    if credit_history_years < 0 or credit_history_years > 80:
        raise ValueError(
            "Credit history must be between 0 and 80 years."
        )


    # --------------------------------------------------------
    # OPEN CREDIT ACCOUNTS
    # --------------------------------------------------------

    open_credit_accounts = data[
        "open_credit_accounts"
    ]

    if (
        open_credit_accounts < 0
        or open_credit_accounts > 100
    ):
        raise ValueError(
            "Open credit accounts must be between "
            "0 and 100."
        )


    # --------------------------------------------------------
    # DEPENDENTS
    # --------------------------------------------------------

    dependents = data["dependents"]

    if dependents < 0 or dependents > 20:
        raise ValueError(
            "Dependents must be between 0 and 20."
        )


    # --------------------------------------------------------
    # MONTHLY EMI
    # --------------------------------------------------------

    monthly_emi = data["monthly_emi"]

    if monthly_emi < 0:
        raise ValueError(
            "Monthly EMI cannot be negative."
        )


    # --------------------------------------------------------
    # DEBT TO INCOME RATIO
    # --------------------------------------------------------

    dti = data["debt_to_income_ratio"]

    if dti < 0 or dti > 10:
        raise ValueError(
            "Debt-to-income ratio must be between 0 and 10."
        )


    # --------------------------------------------------------
    # LOAN TO INCOME RATIO
    # --------------------------------------------------------

    lti = data["loan_to_income_ratio"]

    if lti < 0 or lti > 20:
        raise ValueError(
            "Loan-to-income ratio must be between 0 and 20."
        )


    # --------------------------------------------------------
    # REQUIRED TEXT FIELDS
    # --------------------------------------------------------

    text_fields = [
        "bank",
        "employment_type",
        "home_ownership",
        "loan_purpose",
    ]

    for field in text_fields:

        if not data[field]:

            raise ValueError(
                f"{field.replace('_', ' ').title()} "
                "cannot be empty."
            )


# ============================================================
# 404 ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def page_not_found(error):
    """
    Handles invalid/non-existing URLs.
    """

    return render_template(
        "404.html"
    ), 404


# ============================================================
# 405 METHOD NOT ALLOWED
# ============================================================

@app.errorhandler(405)
def method_not_allowed(error):
    """
    Handles requests using an unsupported HTTP method.
    """

    return render_template(
        "error.html",
        error_code=405,
        error_title="Method Not Allowed",
        error_message=(
            "The requested action is not supported "
            "for this page."
        )
    ), 405


# ============================================================
# 413 REQUEST TOO LARGE
# ============================================================

@app.errorhandler(413)
def request_too_large(error):
    """
    Handles requests exceeding MAX_CONTENT_LENGTH.
    """

    return render_template(
        "error.html",
        error_code=413,
        error_title="Request Too Large",
        error_message=(
            "The submitted request is larger than "
            "the allowed limit."
        )
    ), 413


# ============================================================
# 500 INTERNAL SERVER ERROR
# ============================================================

@app.errorhandler(500)
def internal_server_error(error):
    """
    Global fallback for unexpected Flask errors.
    """

    return render_template(
        "error.html",
        error_code=500,
        error_title="Internal Server Error",
        error_message=(
            "The application encountered an unexpected "
            "error while processing your request."
        )
    ), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )