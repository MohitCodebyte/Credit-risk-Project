import pandas as pd


# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

input_file = "data/raw/RBI_NPA_2025.xlsx"
output_file = "data/processed/bank_risk_benchmark.csv"


# --------------------------------------------------
# 2. Load raw RBI Excel file
# --------------------------------------------------

df = pd.read_excel(
    input_file,
    header=6
)

print("Raw Data Shape:", df.shape)


# --------------------------------------------------
# 3. Clean column names
# --------------------------------------------------

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("%", "percent")
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
)


# --------------------------------------------------
# 4. Remove completely empty rows
# --------------------------------------------------

df = df.dropna(how="all")


# --------------------------------------------------
# 5. Clean text columns
# --------------------------------------------------

df["banks"] = df["banks"].astype(str).str.strip()


# --------------------------------------------------
# 6. Convert numeric columns
# --------------------------------------------------

df["year"] = pd.to_numeric(df["year"], errors="coerce")

df["gross_npas"] = pd.to_numeric(
    df["gross_npas"],
    errors="coerce"
)

df["gross_advances"] = pd.to_numeric(
    df["gross_advances"],
    errors="coerce"
)

df["gross_npas_to_gross_advances_ratio_percent"] = pd.to_numeric(
    df["gross_npas_to_gross_advances_ratio_percent"],
    errors="coerce"
)


# --------------------------------------------------
# 7. Remove completely empty columns
# --------------------------------------------------

df = df.dropna(axis=1, how="all")


# --------------------------------------------------
# 8. Fill merged Year values
# --------------------------------------------------

df["year"] = df["year"].ffill()

# --------------------------------------------------


# --------------------------------------------------
# 9. Display processed data
# --------------------------------------------------

print("\nProcessed Columns:")
print(df.columns.tolist())

print("\nProcessed Data Shape:", df.shape)

print("\nFirst 10 Processed Rows:")
print(df.head(10).to_string(index=False))


# --------------------------------------------------
# 10. Check missing values
# --------------------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())



# --------------------------------------------------
# 11. Investigate missing values
# --------------------------------------------------

missing_rows = df[df.isnull().any(axis=1)]

print("\nRows Containing Missing Values:")
print(missing_rows.to_string(index=False))

print("\nNumber of Rows With Missing Values:", len(missing_rows))

# --------------------------------------------------
# 12. Keep latest RBI reporting year
# --------------------------------------------------

df = df[df["year"] == 2025].copy()

print("\n2025 RBI Data Shape:", df.shape)


# --------------------------------------------------
# 13. Remove records with missing financial values
# --------------------------------------------------

df = df.dropna(
    subset=[
        "banks",
        "gross_npas",
        "gross_advances",
        "gross_npas_to_gross_advances_ratio_percent"
    ]
)

print("\nClean 2025 Data Shape:", df.shape)


# --------------------------------------------------
# 14. Reset index
# --------------------------------------------------

df = df.reset_index(drop=True)

# --------------------------------------------------
# 15. Inspect final 2025 bank dataset
# --------------------------------------------------

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFinal Dataset Columns:")
print(df.columns.tolist())

print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\n2025 Banks in Processed Dataset:")

for bank in df["banks"]:
    print(bank)

print("\nTotal Banks:")
print(df["banks"].nunique())


# --------------------------------------------------
# 16. Basic Data Validation
# --------------------------------------------------

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Bank-Year Records:")
print(
    df.duplicated(
        subset=["year", "banks"]
    ).sum()
)

print("\nData Types:")
print(df.dtypes)


# --------------------------------------------------
# 17. Validate Financial Values
# --------------------------------------------------

print("\nNegative Gross NPA Values:")
print(
    (df["gross_npas"] < 0).sum()
)

print("\nNegative Gross Advances Values:")
print(
    (df["gross_advances"] < 0).sum()
)

print("\nNPA Ratio Range:")
print(
    df[
        "gross_npas_to_gross_advances_ratio_percent"
    ].min(),
    "to",
    df[
        "gross_npas_to_gross_advances_ratio_percent"
    ].max()
)

# --------------------------------------------------
# 18. Save processed data
# --------------------------------------------------

df.to_csv(output_file, index=False)

print("\n----------------------------------------")
print("RBI DATA PREPROCESSING COMPLETED")
print("----------------------------------------")
print("Saved File:", output_file)