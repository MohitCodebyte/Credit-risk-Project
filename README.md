# 💳 Credit Risk Analytics & Loan Default Prediction System

> An end-to-end Machine Learning and Analytics system for assessing borrower credit risk, predicting potential loan default, generating an interpretable 0–100 risk score, and delivering predictions through a Flask-based web application.

---

## 📌 Overview

The **Credit Risk Analytics & Loan Default Prediction System** is an end-to-end Data Science and Machine Learning project that demonstrates how borrower financial information can be analyzed to estimate the probability of loan default.

The project combines **official Reserve Bank of India (RBI) bank-level asset-quality data** with a separately generated **synthetic borrower-level dataset** to build a complete credit-risk analytics workflow.

The system covers the complete journey from:

```text
Data Collection
      ↓
Data Cleaning
      ↓
Data Validation
      ↓
Exploratory Data Analysis
      ↓
Feature Engineering
      ↓
Imbalanced Classification
      ↓
Model Training
      ↓
Model Comparison
      ↓
Hyperparameter Tuning
      ↓
Threshold Optimization
      ↓
Explainable AI
      ↓
Risk Scoring
      ↓
Flask Integration
      ↓
Interactive Web Application
```

The final application allows users to enter borrower information and receive:

- Default probability
- 0–100 credit risk score
- Risk category
- Default prediction
- Risk interpretation
- Explainability-oriented insights

---

# 🎯 Business Problem

Loan default is an important risk for financial institutions.

Before approving or reviewing a loan application, lenders need to evaluate multiple aspects of a borrower's financial profile, such as:

- Credit score
- Annual income
- Existing debt
- Existing loans
- Previous delinquencies
- Previous defaults
- Employment stability
- Loan amount
- Loan term
- Interest rate
- Debt-to-income ratio
- Loan-to-income ratio
- Credit history
- Bank-level credit-risk environment

A simple rule-based approach may not capture the relationships between all these variables.

This project explores a Machine Learning based approach that estimates the probability of default and converts that probability into an easy-to-understand **0–100 Credit Risk Score**.

---

# 💡 Project Objectives

The major objectives of the project are:

1. Collect authentic bank-level financial risk data from the RBI.
2. Clean and validate the raw RBI dataset.
3. Build a structured bank-level NPA benchmark.
4. Generate a borrower-level synthetic dataset for ML experimentation.
5. Perform Exploratory Data Analysis.
6. Engineer financially meaningful features.
7. Handle class imbalance using SMOTE.
8. Train multiple Machine Learning classification models.
9. Compare model performance using multiple metrics.
10. Perform stratified cross-validation.
11. Perform hyperparameter tuning.
12. Optimize the classification threshold.
13. Implement SHAP-based model explainability.
14. Convert default probability into a 0–100 risk score.
15. Categorize borrowers into risk levels.
16. Integrate the trained model into Flask.
17. Build an interactive analytics dashboard.
18. Prepare the application for deployment.

---

# 🏦 Data Collection

## 1. Official RBI Data

The bank-level benchmark used in this project comes from publicly available information published by the **Reserve Bank of India (RBI)**.

The RBI provides bank-wise and bank-group-wise asset-quality information including:

- Gross Non-Performing Assets (Gross NPAs)
- Gross Advances
- Gross NPA Ratio

The project uses RBI's:

```text
Gross and Net NPAs of Scheduled Commercial Banks
Bank Group-Wise
```

along with bank-wise information containing:

```text
Bank
Gross NPAs
Gross Advances
Gross NPA to Gross Advances Ratio (%)
```

The project uses the **2025 reporting period** as the bank-level benchmark.

### Why RBI?

Instead of manually inventing bank-level risk information, the project uses an authentic external financial-sector source.

The RBI data provides a real-world bank-level benchmark that can be associated with selected banks in the borrower-level modeling dataset.

---

# ⚠️ Data Transparency

A key design decision in this project is the separation between **real external financial data** and **synthetic borrower-level data**.

## ✅ Real Data — RBI

The following information comes from the official RBI source:

```text
Bank-level Gross NPAs
Bank-level Gross Advances
Bank-level Gross NPA Ratio
```

This data was downloaded, processed, cleaned and validated before being used as the bank-risk benchmark.

## 🧪 Synthetic Data — Borrower Level

Individual borrower loan/customer records are generally not publicly available in the required form.

Therefore, a separate borrower-level dataset was generated for Machine Learning experimentation.

The synthetic dataset contains borrower attributes such as:

```text
Age
Employment Type
Employment Length
Annual Income
Credit Score
Loan Amount
Loan Term
Interest Rate
Existing Debt
Existing Loans
Previous Delinquencies
Previous Defaults
Credit History
Open Credit Accounts
Dependents
Home Ownership
Loan Purpose
Monthly Income
Monthly EMI
Debt-to-Income Ratio
Loan-to-Income Ratio
Default Flag
```

### Important

The borrower dataset is **synthetic** and was created for educational and Machine Learning development purposes.

The synthetic **7% default rate is a characteristic of the generated dataset** and should not be interpreted as the actual borrower default rate of the Indian banking system.

The project does **not** claim that the borrower-level records represent real bank customers.

---

# 🔄 Data Science Methodology

## Step 1 — RBI Data Processing

The raw RBI Excel dataset was not directly passed into the Machine Learning model.

It first went through a preprocessing and validation pipeline.

```text
Official RBI Excel File
        ↓
Load Excel Dataset
        ↓
Clean Column Names
        ↓
Remove Empty Rows / Columns
        ↓
Forward Fill Year Information
        ↓
Filter 2025 Reporting Period
        ↓
Remove Missing Financial Records
        ↓
Validate Data Types
        ↓
Check Duplicate Records
        ↓
Check Negative Financial Values
        ↓
Validate NPA Ratios
        ↓
Processed RBI Benchmark
```

Implementation:

```text
src/data_preprocessing.py
```

Output:

```text
data/processed/bank_risk_benchmark.csv
```

---

# 🔍 Data Validation

The processed RBI dataset was validated for:

- Missing values
- Duplicate rows
- Duplicate bank-year combinations
- Negative Gross NPA values
- Negative Gross Advances
- Invalid NPA ratios
- Data-type consistency

The final processed dataset provides a clean bank-level benchmark for the selected reporting period.

---

# 👥 Step 2 — Synthetic Borrower Dataset

Because the RBI dataset contains aggregate bank-level information rather than individual borrower records, a separate borrower-level dataset was created.

The dataset contains:

```text
10,000 Borrowers
20 Selected Banks
28 Original Features
```

Generation script:

```text
src/generate_borrower_data.py
```

Generated dataset:

```text
data/synthetic/borrower_credit_data.csv
```

The synthetic data generation process was designed to create meaningful relationships between borrower characteristics and credit-risk behavior.

---

# 🧠 Synthetic Risk Generation Logic

The synthetic borrower-generation process considers multiple risk-related characteristics.

Examples include:

- Lower credit scores
- Higher debt-to-income ratio
- Higher loan-to-income ratio
- Previous delinquencies
- Previous defaults
- Higher interest rates
- Employment stability
- Bank-level Gross NPA Ratio

The objective was not to reproduce real customer records.

The objective was to create a structured dataset suitable for demonstrating a complete **Credit Risk Machine Learning workflow**.

---

# 🔗 Connecting RBI Data with Borrower Data

After processing the RBI dataset, the bank-level Gross NPA Ratio was mapped to the selected banks in the synthetic borrower dataset.

This created the contextual feature:

```text
bank_gross_npa_ratio
```

Conceptually:

```text
                    RBI Bank-Level Data
                           │
                           ▼
                  Bank Gross NPA Ratio
                           │
                           ▼
                 ┌───────────────────┐
                 │ Selected Bank      │
                 │ Risk Benchmark     │
                 └─────────┬─────────┘
                           │
                           ▼
Borrower ───────► bank_gross_npa_ratio
    │
    ├── Credit Score
    ├── Income
    ├── Loan Amount
    ├── Existing Debt
    ├── Previous Defaults
    └── Other Financial Features
```

This allows the project to combine:

```text
Borrower-Level Risk
        +
Bank-Level Risk Context
```

while maintaining a clear distinction between official aggregate data and synthetic borrower data.

---

# 📊 Exploratory Data Analysis

Before training Machine Learning models, extensive Exploratory Data Analysis was performed.

## Numerical Analysis

The analysis included:

- Age distribution
- Income distribution
- Credit score distribution
- Loan amount distribution
- Interest rate distribution
- Existing debt distribution
- Monthly EMI distribution
- Debt-to-income ratio
- Loan-to-income ratio

## Default Analysis

Default behavior was analyzed against:

- Credit score
- Income
- Loan amount
- Existing debt
- Previous delinquencies
- Previous defaults
- Interest rate
- Debt-to-income ratio
- Loan-to-income ratio

## Categorical Analysis

The project also analyzed:

- Employment type
- Home ownership
- Loan purpose
- Bank

## Risk Analysis

Default rates were also examined across:

- Generated risk categories
- Selected banks
- Borrower characteristics

EDA notebook:

```text
notebooks/02_eda_credit_risk.ipynb
```

---

# ⚙️ Feature Engineering

Several additional features were engineered to represent borrower financial risk more meaningfully.

## 1. EMI-to-Income Ratio

```text
EMI-to-Income Ratio
=
Monthly EMI / Monthly Income
```

This represents the proportion of monthly income required for the loan EMI.

---

## 2. Total Debt Exposure

```text
Total Debt Exposure
=
Existing Debt + Loan Amount
```

This represents the borrower's combined debt exposure after considering the requested loan.

---

## 3. Credit History Age Ratio

```text
Credit History Age Ratio
=
Credit History Years / Age
```

This provides a normalized representation of credit history relative to borrower age.

---

## 4. Previous Delinquency Indicator

```text
Has Previous Delinquency
=
1 if Previous Delinquencies > 0
0 otherwise
```

This gives the model a direct indicator of previous repayment issues.

Feature engineering notebook:

```text
notebooks/03_feature_engineering.ipynb
```

---

# ⚖️ Handling Class Imbalance

The target variable contains significantly fewer default cases than non-default cases.

Therefore, class imbalance was handled using:

```text
SMOTE
```

### SMOTE

**SMOTE — Synthetic Minority Over-sampling Technique**

SMOTE was applied **only within the training pipeline**.

The test dataset was kept untouched so that evaluation remained based on the original test distribution.

Conceptually:

```text
Training Data
      ↓
Preprocessing
      ↓
SMOTE
      ↓
Balanced Training Data
      ↓
Model
```

while:

```text
Test Data
      ↓
Original Distribution
      ↓
Evaluation
```

This helps avoid artificially modifying the test distribution during model evaluation.

---

# 🤖 Machine Learning Models

Four classification algorithms were trained and compared:

| Model | Type |
|---|---|
| Logistic Regression | Linear Classification |
| Random Forest | Ensemble Tree Model |
| XGBoost | Gradient Boosting |
| LightGBM | Gradient Boosting |

The purpose of model comparison was to evaluate different modeling approaches instead of assuming a particular algorithm would perform best beforehand.

---

# 📏 Model Evaluation

Because this is an imbalanced classification problem, accuracy was not treated as the only evaluation metric.

The following metrics were evaluated:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- PR-AUC

### Recall

Recall is particularly relevant when identifying potential default cases because false negatives can represent borrowers who default but were not flagged by the model.

### Precision

Precision helps measure how many borrowers flagged as potential defaults were actually default cases within the evaluation dataset.

### PR-AUC

PR-AUC is useful for evaluating performance when the positive class is relatively small.

### ROC-AUC

ROC-AUC measures discrimination between default and non-default cases across different probability thresholds.

---

# 🔬 Cross Validation & Hyperparameter Tuning

The project used:

```text
5-Fold Stratified Cross Validation
```

for model evaluation.

Hyperparameter optimization was performed using:

```text
RandomizedSearchCV
```

The tuning objective used:

```text
Average Precision / PR-AUC
```

This metric was selected because the project deals with an imbalanced target.

---

# 🎚️ Classification Threshold Optimization

A Machine Learning classifier does not necessarily need to use the default probability threshold of `0.50`.

Therefore, multiple thresholds were evaluated to study the precision-recall trade-off.

The current project configuration uses:

```text
Classification Threshold = 0.58
```

The threshold is stored separately:

```text
models/credit_risk_threshold.pkl
```

Current prediction logic:

```text
Predicted Probability >= 0.58
             ↓
      Potential Default

Predicted Probability < 0.58
             ↓
     Lower Default Risk
```

The threshold is a **project-specific modeling configuration**, not a universal banking threshold.

---

# 🏁 Final Model

The current deployed project configuration uses a tuned:

```text
Logistic Regression
```

with:

```text
Classification Threshold = 0.58
```

Saved model:

```text
models/credit_risk_model.pkl
```

The model selection was based on the project's validation, evaluation and threshold analysis.

This result should not be interpreted as a claim that Logistic Regression is universally superior for credit-risk modeling.

---

# 🔬 Explainable AI — SHAP

To make the model more interpretable, **SHAP (SHapley Additive exPlanations)** was used.

SHAP analysis helps understand which features contribute to model predictions and provides insight into overall feature importance.

Important features identified during the analysis include:

```text
Credit Score
Debt-to-Income Ratio
Previous Delinquencies
Previous Defaults
Interest Rate
Home Ownership
Employment Length
Employment Type
EMI-to-Income Ratio
```

Generated outputs:

```text
reports/
├── shap_feature_importance.csv
└── figures/
    ├── shap_summary.png
    └── shap_feature_importance.png
```

---

# 🎯 Credit Risk Score

The trained model produces a probability of default.

For easier interpretation, the probability is converted into a 0–100 risk score.

```text
Risk Score
=
Default Probability × 100
```

Example:

```text
Default Probability = 0.32

Risk Score = 32
```

Therefore:

```text
0% Probability  →  0 Risk Score
50% Probability → 50 Risk Score
100% Probability → 100 Risk Score
```

Higher scores represent higher predicted default risk.

---

# 🚦 Risk Classification

The application converts the risk score into four categories:

| Risk Score | Category |
|---:|---|
| 0 – 24.99 | Low Risk |
| 25 – 49.99 | Medium Risk |
| 50 – 74.99 | High Risk |
| 75 – 100 | Very High Risk |

```text
0 ───────── 25 ───────── 50 ───────── 75 ───────── 100
     Low          Medium        High        Very High
```

---

# 🌐 Flask Web Application

After model development, the trained Machine Learning pipeline was integrated into a Flask application.

The web application workflow is:

```text
User
  ↓
Borrower Assessment Form
  ↓
Input Validation
  ↓
Feature Preparation
  ↓
Saved ML Pipeline
  ↓
Default Probability
  ↓
Risk Score
  ↓
Risk Category
  ↓
Prediction Result
```

The inference logic is separated into:

```text
src/inference.py
```

while the Flask application is handled by:

```text
app/app.py
```

This separation allows the trained model to be reused for predictions without retraining the model for every request.

---

# 🖥️ Application Pages

The web application contains dedicated pages for different parts of the system.

### 🏠 Home / Assessment

Provides:

- Project introduction
- Borrower assessment form
- Input validation
- Risk assessment interface

### 📊 Prediction Result

Displays:

- Default probability
- Risk score
- Risk category
- Default prediction
- Risk interpretation

### 📈 Dashboard

Provides analytical views such as:

- Borrower statistics
- Default distribution
- Risk distribution
- Bank-level risk
- Model performance
- Feature importance
- Borrower analytics

### 🧠 Methodology

Explains:

- Data pipeline
- Feature engineering
- SMOTE
- Model training
- Model evaluation
- Threshold optimization
- SHAP
- Risk scoring

### ℹ️ About

Explains:

- Project objective
- Data foundation
- Technology stack
- System architecture
- Project scope

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │       RBI Data          │
                         │   Bank-Level NPA Data   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Data Cleaning &          │
                         │ Validation               │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Bank Risk Benchmark     │
                         │ Dataset                  │
                         └────────────┬────────────┘
                                      │
                                      ▼
                  ┌─────────────────────────────────────┐
                  │ Synthetic Borrower Dataset          │
                  │ 10,000 Records / 20 Selected Banks │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                         ┌─────────────────────────┐
                         │ Exploratory Data        │
                         │ Analysis                │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Feature Engineering     │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Train / Test Split      │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Preprocessing            │
                         │ • Imputation             │
                         │ • Scaling                │
                         │ • One-Hot Encoding      │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │         SMOTE            │
                         │   Class Imbalance        │
                         └────────────┬────────────┘
                                      │
                                      ▼
              ┌─────────────────────────────────────────────┐
              │              Model Training                 │
              │                                             │
              │ Logistic Regression                         │
              │ Random Forest                               │
              │ XGBoost                                     │
              │ LightGBM                                    │
              └──────────────────────┬──────────────────────┘
                                     │
                                     ▼
                         ┌─────────────────────────┐
                         │ Hyperparameter Tuning   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Threshold Optimization  │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Final Credit Risk Model │
                         └────────────┬────────────┘
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
               ┌──────────────────┐      ┌──────────────────┐
               │ SHAP Explainable │      │ Risk Score       │
               │ AI Analysis      │      │ 0 – 100          │
               └──────────────────┘      └────────┬─────────┘
                                                   │
                                                   ▼
                                      ┌────────────────────┐
                                      │ Flask Web App      │
                                      └─────────┬──────────┘
                                                │
                                                ▼
                                      ┌────────────────────┐
                                      │ User Prediction    │
                                      │ Dashboard          │
                                      │ Result Analysis    │
                                      └────────────────────┘
```

---

# 🗂️ Project Structure

```text
Credit-Risk-Analytics-System/
│
├── 📁 app/
│   ├── 📄 __init__.py
│   │   └── Flask application package initializer
│   │
│   ├── 📄 app.py
│   │   └── Main Flask backend
│   │       ├── Home route
│   │       ├── Dashboard route
│   │       ├── About route
│   │       ├── Methodology route
│   │       ├── Prediction route
│   │       ├── Error handlers
│   │       └── 404 handler
│   │
│   ├── 📁 templates/
│   │   ├── 📄 index.html
│   │   ├── 📄 result.html
│   │   ├── 📄 dashboard.html
│   │   ├── 📄 about.html
│   │   ├── 📄 methodology.html
│   │   ├── 📄 error.html
│   │   └── 📄 404.html
│   │
│   └── 📁 static/
│       ├── 📁 css/
│       │   └── 📄 style.css
│       │       └── Application styling and UI design
│       │
│       ├── 📁 js/
│       │   └── 📄 app.js
│       │       └── Frontend interactions, animations,
│       │           validation and UI behavior
│       │
│       ├── 📁 images/
│       └── 📁 icons/
│
├── 📁 data/
│   ├── 📁 raw/
│   │   └── 📄 RBI_NPA_2025.xlsx
│   │       └── Raw RBI bank-level dataset
│   │
│   ├── 📁 processed/
│   │   └── 📄 bank_risk_benchmark.csv
│   │       └── Cleaned RBI bank-risk benchmark
│   │
│   └── 📁 synthetic/
│       └── 📄 borrower_credit_data.csv
│           └── Synthetic borrower-level dataset
│
├── 📁 models/
│   ├── 📄 credit_risk_model.pkl
│   │   └── Serialized trained ML pipeline
│   │
│   ├── 📄 credit_risk_threshold.pkl
│   │   └── Optimized classification threshold
│   │
│   └── 📄 risk_scoring_config.pkl
│       └── Risk-score configuration
│
├── 📁 notebooks/
│   ├── 📄 02_eda_credit_risk.ipynb
│   │   └── Exploratory Data Analysis
│   │
│   ├── 📄 03_feature_engineering.ipynb
│   │   └── Feature engineering workflow
│   │
│   └── 📄 04_model_training.ipynb
│       └── Model training, comparison,
│           tuning and threshold analysis
│
├── 📁 reports/
│   ├── 📄 shap_feature_importance.csv
│   │   └── SHAP feature importance results
│   │
│   └── 📁 figures/
│       ├── 📄 shap_summary.png
│       └── 📄 shap_feature_importance.png
│
├── 📁 src/
│   ├── 📄 data_preprocessing.py
│   │   └── RBI data cleaning and validation
│   │
│   ├── 📄 generate_borrower_data.py
│   │   └── Synthetic borrower dataset generation
│   │
│   └── 📄 inference.py
│       └── Production inference and risk prediction logic
│
├── 📁 dashboard/
│   └── Dashboard-related project resources
│
├── 📄 requirements.txt
│   └── Python dependencies
│
├── 📄 README.md
│   └── Project documentation
│
├── 📄 .gitignore
│   └── Git ignored files and environment exclusions
│
└── 📄 LICENSE
    └── Project license
```

---

# 📊 Project at a Glance

| Component | Details |
|---|---|
| External Data Source | Reserve Bank of India |
| Reporting Period | 2025 |
| Borrower Records | 10,000 |
| Selected Banks | 20 |
| Default Records | 700 |
| Non-Default Records | 9,300 |
| Synthetic Default Rate | 7% |
| Train/Test Split | 80/20 |
| ML Models | 4 |
| Imbalance Handling | SMOTE |
| Hyperparameter Tuning | RandomizedSearchCV |
| Cross Validation | 5-Fold Stratified CV |
| Explainability | SHAP |
| Final Model | Tuned Logistic Regression |
| Classification Threshold | 0.58 |
| Risk Score | 0–100 |
| Risk Categories | 4 |
| Backend | Flask |
| Model Serialization | Joblib |
| Deployment Stack | Gunicorn + Render |

---

# 🛠️ Technology Stack

## Data Science

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- OpenPyXL

## Machine Learning

- Scikit-learn
- Imbalanced-learn
- XGBoost
- LightGBM
- SHAP
- Joblib

## Backend

- Flask
- Python
- Gunicorn

## Frontend

- HTML5
- CSS3
- JavaScript

## Development & Deployment

- Jupyter Notebook
- Git
- GitHub
- Render

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Credit-Risk-Analytics-System
```

## 2. Create Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app/app.py
```

Open the local application:

```text
http://127.0.0.1:5000
```

---

# 🧪 Example Prediction Flow

A user enters borrower information:

```text
Credit Score
Annual Income
Loan Amount
Loan Term
Interest Rate
Existing Debt
Previous Defaults
Previous Delinquencies
Employment Information
Loan Purpose
Bank
...
```

The application then performs:

```text
Input
 ↓
Validation
 ↓
Feature Engineering
 ↓
Preprocessing
 ↓
Saved ML Pipeline
 ↓
Default Probability
 ↓
Risk Score
 ↓
Risk Category
 ↓
Prediction Result
```

Example output:

```text
Default Probability: 3.06%
Risk Score: 3.06
Risk Category: Low Risk
Prediction: Lower Default Risk
```

---

# 🔐 Model & Application Safety

The application includes input validation and error handling for invalid or unexpected requests.

The model is loaded from serialized artifacts rather than retrained during every prediction.

Important model files:

```text
models/
├── credit_risk_model.pkl
├── credit_risk_threshold.pkl
└── risk_scoring_config.pkl
```

---

# 📈 Key Machine Learning Concepts Demonstrated

This project demonstrates practical implementation of:

```text
Data Collection
Data Cleaning
Data Validation
EDA
Feature Engineering
Train/Test Split
Data Preprocessing
Categorical Encoding
Feature Scaling
Class Imbalance
SMOTE
Classification
Cross Validation
Hyperparameter Tuning
Threshold Optimization
Model Evaluation
SHAP Explainability
Probability-Based Risk Scoring
Model Serialization
Model Inference
Flask Deployment
```

---

# 💼 My Contribution

I independently designed and implemented the complete project workflow, including:

- Identified the credit-risk business problem
- Collected official RBI bank-level NPA data
- Processed and validated the RBI Excel dataset
- Built the cleaned bank-risk benchmark
- Designed and generated the synthetic borrower-level dataset
- Performed Exploratory Data Analysis
- Engineered financially meaningful features
- Built preprocessing pipelines
- Handled class imbalance using SMOTE
- Trained multiple Machine Learning models
- Compared models using multiple evaluation metrics
- Performed stratified cross-validation
- Performed hyperparameter tuning
- Optimized the classification threshold
- Implemented SHAP-based explainability
- Built the 0–100 credit-risk scoring system
- Serialized the trained model using Joblib
- Integrated the ML pipeline with Flask
- Developed the web interface
- Built analytics and visualization pages
- Implemented input validation and error handling
- Prepared the application for deployment

---

# 🌟 What Makes This Project Different

This project goes beyond a basic:

```text
Dataset → Model → Accuracy
```

approach.

Instead, it demonstrates a complete end-to-end workflow:

```text
Official External Financial Data
            +
Data Engineering
            +
Data Validation
            +
Synthetic Borrower Modeling Dataset
            +
EDA
            +
Feature Engineering
            +
Imbalanced Learning
            +
Multiple ML Models
            +
Cross Validation
            +
Hyperparameter Tuning
            +
Threshold Optimization
            +
Explainable AI
            +
Risk Scoring
            +
Flask Backend
            +
Interactive Frontend
            +
Deployment
```

The project therefore demonstrates both **Data Science capability** and the ability to convert a trained model into a usable application.

---

# ⚠️ Limitations

This project has several important limitations:

### 1. Synthetic Borrower Data

The borrower-level dataset is synthetic and is not a collection of real bank customers.

### 2. Limited Bank-Level Context

The RBI information used here is aggregate bank-level information rather than individual customer-level banking history.

### 3. No Confidential Banking Data

The model has not been trained or validated on confidential bank customer data.

### 4. Model Generalization

Performance observed during development applies to the synthetic dataset used in this project and should not be assumed to represent performance on real-world banking populations.

### 5. Production Credit Decisions

The system is an educational and portfolio project and should not be used by a financial institution to automatically approve or reject actual loans.

---

# 🔮 Future Improvements

Possible future improvements include:

- Integration with a larger real-world borrower dataset where legally available
- Real-time financial data pipelines
- MySQL-based borrower and prediction history
- User authentication and role-based access
- Loan application management
- Model monitoring
- Data drift detection
- Probability calibration
- Cost-sensitive learning
- Advanced threshold optimization based on business cost
- Additional ensemble models
- Automated model retraining
- Model versioning
- REST API deployment
- Docker containerization
- Cloud database integration
- Advanced Power BI analytics
- Audit logs for predictions
- Fairness and bias analysis

---

# 📚 Learning Outcomes

Through this project, I gained practical experience in:

- Real-world financial data processing
- Working with official statistical datasets
- Data cleaning and validation
- Synthetic data generation
- Exploratory Data Analysis
- Financial feature engineering
- Imbalanced classification
- SMOTE
- Model comparison
- Cross-validation
- Hyperparameter optimization
- Precision-recall trade-offs
- Classification threshold selection
- Explainable AI
- Model serialization
- Flask model deployment
- Building production-oriented ML workflows

---

# 🎤 Interview Explanation

A concise explanation of the project:

> “I built an end-to-end Credit Risk Analytics and Loan Default Prediction System. I first collected official bank-level asset-quality data from the RBI and processed it into a clean NPA benchmark. Since individual borrower-level loan data was not publicly available in the required form, I created a separate synthetic borrower dataset for ML experimentation and clearly documented that distinction.
>
> I performed EDA and feature engineering, including EMI-to-income ratio, total debt exposure and credit-history age ratio. Since default cases were imbalanced, I used SMOTE only within the training pipeline. I compared Logistic Regression, Random Forest, XGBoost and LightGBM using metrics such as Precision, Recall, F1, ROC-AUC and PR-AUC.
>
> I then performed stratified cross-validation, RandomizedSearchCV-based hyperparameter tuning and classification-threshold optimization. The current project configuration uses a tuned Logistic Regression model with a 0.58 threshold.
>
> For interpretability, I implemented SHAP analysis and converted the model's default probability into a 0–100 risk score with four risk categories. Finally, I integrated the trained pipeline into a Flask web application with an interactive frontend and analytics dashboard.”

---

# 📌 Resume Project Description

### Credit Risk Analytics & Loan Default Prediction System

**Python, Pandas, NumPy, Scikit-learn, XGBoost, LightGBM, SMOTE, SHAP, Flask**

- Built an end-to-end credit-risk ML system using official RBI bank-level NPA data as a financial benchmark and a separate synthetic borrower-level dataset for model development.
- Performed data cleaning, validation, EDA and financial feature engineering including DTI, LTI, EMI-to-income and total debt exposure.
- Compared Logistic Regression, Random Forest, XGBoost and LightGBM using Precision, Recall, F1, ROC-AUC and PR-AUC with SMOTE-based imbalance handling.
- Applied 5-fold stratified cross-validation, RandomizedSearchCV, threshold optimization and SHAP explainability.
- Developed a Flask-based prediction application that converts default probability into a 0–100 risk score and four risk categories.

---

# 📎 Data Source

Official Reserve Bank of India statistical data was used for the bank-level NPA benchmark.

The borrower-level dataset is explicitly synthetic and was created for educational and Machine Learning development purposes.

---

# ⚖️ Disclaimer

This project is intended for **educational, portfolio and Machine Learning development purposes only**.

The bank-level benchmark data is sourced from publicly available official RBI information.

The borrower-level dataset is synthetic.

The model has not been validated using confidential bank customer data and should not be used for actual loan approval, rejection, credit underwriting, or other financial decision-making.

Model performance reported in this repository applies to the synthetic dataset used during development.

---

# 👨‍💻 Author

**Mohit Kushwah**

B.Tech — Computer Science & Engineering

Interested in:

- Data Science
- Machine Learning
- Data Analytics
- Python Development
- Backend Development

---

# ⭐ Project Highlights

```text
✔ Official RBI financial data
✔ Transparent data methodology
✔ 10,000 synthetic borrower records
✔ 20 selected banks
✔ Complete EDA pipeline
✔ Financial feature engineering
✔ SMOTE for class imbalance
✔ 4 ML classification models
✔ 5-Fold Stratified Cross Validation
✔ Hyperparameter Tuning
✔ Threshold Optimization
✔ SHAP Explainable AI
✔ 0–100 Risk Scoring
✔ Flask ML Integration
✔ Interactive Web Interface
✔ Analytics Dashboard
✔ Production-oriented project structure
✔ Deployment-ready architecture
```

---

# 📄 License

This project is intended for educational and portfolio purposes.

See the `LICENSE` file for license information.

---

<p align="center">

### 💳 Credit Risk Analytics & Loan Default Prediction System

**Built with Python • Machine Learning • Explainable AI • Flask**

**Developed by Mohit Kushwah**

</p>