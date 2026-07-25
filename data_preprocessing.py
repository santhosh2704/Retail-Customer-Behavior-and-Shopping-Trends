import pandas as pd
from database_connection import engine

# Load Dataset

df = pd.read_csv(
    r"E:\Projects\Retail Customer Behavior and Shopping Trends\data\customer_shopping_behavior.csv"
)

# Basic Data Exploration

print("\nFirst 5 Rows")
print(df.head())

print("\nDataset Information")
print(df.info())

print("\nNumerical Summary")
print(df.describe())

print("\nComplete Summary")
print(df.describe(include="all"))

print("\nMissing Values")
print(df.isnull().sum())

# Fill Missing Review Ratings

df["Review Rating"] = (
    df.groupby("Category")["Review Rating"]
    .transform(lambda x: x.fillna(x.median()))
)

print("\nMissing Values After Cleaning")
print(df.isnull().sum())

# Standardize Column Names

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ", "_")

print("\nColumn Names")
print(df.columns)

# Rename Column

df = df.rename(
    columns={
        "purchase_amount_(usd)": "purchase_amount"
    }
)

print("\nUpdated Column Names")
print(df.columns)

# Create Age Groups

labels = [
    "Young Adult",
    "Adult",
    "Middle Ages",
    "Senior"
]

df["age_group"] = pd.qcut(
    df["age"],
    q=4,
    labels=labels
)

print("\nAge Groups")
print(df[["age", "age_group"]].head(10))

# Convert Purchase Frequency into Days

frequency_mapping = {
    "Fortnightly": 14,
    "Weekly": 7,
    "Monthly": 30,
    "Quarterly": 90,
    "Bi-Weekly": 14,
    "Annually": 365,
    "Every 3 Months": 90
}

df["purchase_frequency_days"] = (
    df["frequency_of_purchases"]
    .map(frequency_mapping)
)

print("\nPurchase Frequency")
print(
    df[
        [
            "frequency_of_purchases",
            "purchase_frequency_days"
        ]
    ].head(10)
)

# Check Duplicate Columns

print("\nDiscount Applied == Promo Code Used")

print((df["discount_applied"]==df["promo_code_used"]).all())

# Drop Promo Code Column

df = df.drop(columns="promo_code_used")

print("\nRemaining Columns")
print(df.columns)

# Upload Data to PostgreSQL

df.to_sql(
    "customer_shopping",
    engine,
    if_exists="replace",
    index=False
)

print("\nData uploaded successfully to PostgreSQL!")

