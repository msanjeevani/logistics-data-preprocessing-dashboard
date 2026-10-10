
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================================
# WEEK 2: LOGISTICS DATA COLLECTION, CLEANING & PREPROCESSING
# Dataset: Synthetic / Simulated Logistics Data
# ==========================================================

np.random.seed(42)
sns.set_theme(style="whitegrid")

# STEP 0: Create output folder
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 65)
print("WEEK 2: LOGISTICS DATA PREPROCESSING PIPELINE")
print("=" * 65)

# ==========================================================
# STEP 1: CREATE SYNTHETIC LOGISTICS DATASET
# ==========================================================

n_rows = 1500

raw_data = {
    "order_id": [f"ORD_{i:04d}" for i in range(n_rows)],
    "delivery_time_minutes": np.random.normal(48, 16, n_rows),
    "distance_km": np.random.uniform(2.5, 28.0, n_rows),
    "package_weight_kg": np.random.uniform(0.5, 18.0, n_rows),
    "fuel_cost_usd": np.random.uniform(4.0, 30.0, n_rows),
    "traffic_index": np.random.randint(1, 6, n_rows),
    "weather_condition": np.random.choice(
        ["Clear", "Rainy", "Foggy", "Stormy"],
        size=n_rows,
        p=[0.60, 0.25, 0.10, 0.05]
    ),
    "vehicle_type": np.random.choice(
        ["Van", "Bike", "Truck"],
        size=n_rows,
        p=[0.50, 0.40, 0.10]
    ),
}

df = pd.DataFrame(raw_data)

# Introduce missing values for cleaning practice
df.loc[
    np.random.choice(df.index, 80, replace=False),
    "delivery_time_minutes"
] = np.nan

df.loc[
    np.random.choice(df.index, 50, replace=False),
    "distance_km"
] = np.nan

df.loc[
    np.random.choice(df.index, 60, replace=False),
    "weather_condition"
] = np.nan

# Introduce sample anomalies
df.loc[0, "delivery_time_minutes"] = 310.0
df.loc[1, "delivery_time_minutes"] = -20.0

# Add duplicate records
df = pd.concat([df, df.iloc[:20]], ignore_index=True)

# Save raw dataset
raw_path = os.path.join(OUTPUT_DIR, "raw_logistics_data.csv")
df.to_csv(raw_path, index=False)

raw_row_count = len(df)
missing_before = int(df.isna().sum().sum())
duplicates_before = int(df.duplicated().sum())

print(f"\nRaw dataset shape: {df.shape}")
print(f"Missing cells before cleaning: {missing_before}")
print(f"Duplicate rows before cleaning: {duplicates_before}")

# ==========================================================
# STEP 2: REMOVE DUPLICATES
# ==========================================================

rows_before_deduplication = len(df)

df = df.drop_duplicates().copy()

duplicates_removed = rows_before_deduplication - len(df)

print(f"\nDuplicate rows removed: {duplicates_removed}")

# ==========================================================
# STEP 3: DATA TYPE AND DATA QUALITY VALIDATION
# ==========================================================

numeric_columns = [
    "delivery_time_minutes",
    "distance_km",
    "package_weight_kg",
    "fuel_cost_usd",
    "traffic_index",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Count invalid values before replacing them
invalid_delivery_count = int(
    (df["delivery_time_minutes"] <= 0).sum()
)
invalid_distance_count = int((df["distance_km"] <= 0).sum())
invalid_weight_count = int((df["package_weight_kg"] <= 0).sum())
invalid_fuel_count = int((df["fuel_cost_usd"] <= 0).sum())
invalid_traffic_count = int(
    (~df["traffic_index"].between(1, 5)).sum()
)

# Invalid numeric values become missing values
df.loc[
    df["delivery_time_minutes"] <= 0,
    "delivery_time_minutes"
] = np.nan

df.loc[df["distance_km"] <= 0, "distance_km"] = np.nan

df.loc[
    df["package_weight_kg"] <= 0,
    "package_weight_kg"
] = np.nan

df.loc[df["fuel_cost_usd"] <= 0, "fuel_cost_usd"] = np.nan

df.loc[
    ~df["traffic_index"].between(1, 5),
    "traffic_index"
] = np.nan

print("\nInvalid values detected:")
print(f"Delivery times: {invalid_delivery_count}")
print(f"Distances: {invalid_distance_count}")
print(f"Package weights: {invalid_weight_count}")
print(f"Fuel costs: {invalid_fuel_count}")
print(f"Traffic indexes: {invalid_traffic_count}")

# ==========================================================
# STEP 4: HANDLE MISSING VALUES
# Numerical columns -> median
# Categorical columns -> mode
# ==========================================================

imputed_counts = {}

for column in numeric_columns:
    missing_count = int(df[column].isna().sum())
    imputed_counts[column] = missing_count

    if df[column].notna().any():
        df[column] = df[column].fillna(df[column].median())
    else:
        raise ValueError(
            f"Cannot impute {column}: no valid values available."
        )

categorical_columns = ["weather_condition", "vehicle_type"]

for column in categorical_columns:
    missing_count = int(df[column].isna().sum())
    imputed_counts[column] = missing_count

    if df[column].notna().any():
        df[column] = df[column].fillna(
            df[column].mode().iloc[0]
        )
    else:
        raise ValueError(
            f"Cannot impute {column}: no valid categories available."
        )

print("\nMissing values handled successfully.")

# ==========================================================
# STEP 5: OUTLIER DETECTION USING IQR
# ==========================================================

q1 = df["delivery_time_minutes"].quantile(0.25)
q3 = df["delivery_time_minutes"].quantile(0.75)
iqr = q3 - q1

lower_limit = max(0.0, q1 - 1.5 * iqr)
upper_limit = q3 + 1.5 * iqr

outlier_mask = (
    (df["delivery_time_minutes"] < lower_limit)
    | (df["delivery_time_minutes"] > upper_limit)
)

outliers_removed = int(outlier_mask.sum())

df_cleaned = df.loc[~outlier_mask].copy()

print("\nIQR OUTLIER DETECTION")
print(f"Q1: {q1:.2f}")
print(f"Q3: {q3:.2f}")
print(f"IQR: {iqr:.2f}")
print(f"Lower limit: {lower_limit:.2f}")
print(f"Upper limit: {upper_limit:.2f}")
print(f"Outlier rows removed: {outliers_removed}")

# ==========================================================
# STEP 6: FEATURE ENGINEERING
# ==========================================================

# Average delivery speed in km/h
df_cleaned["avg_speed_kmh"] = (
    df_cleaned["distance_km"]
    / (df_cleaned["delivery_time_minutes"] / 60.0)
)

# Fuel cost per kilometre
df_cleaned["cost_per_km"] = (
    df_cleaned["fuel_cost_usd"]
    / df_cleaned["distance_km"]
)

print("\nFeature engineering completed:")
print("- avg_speed_kmh")
print("- cost_per_km")

# ==========================================================
# STEP 7: MIN-MAX NORMALIZATION
# Values are scaled to the range 0 to 1
# ==========================================================

normalization_columns = [
    "distance_km",
    "package_weight_kg",
    "avg_speed_kmh",
    "fuel_cost_usd",
]

for column in normalization_columns:
    minimum = df_cleaned[column].min()
    maximum = df_cleaned[column].max()

    normalized_column = f"{column}_normalized"

    if maximum > minimum:
        df_cleaned[normalized_column] = (
            (df_cleaned[column] - minimum)
            / (maximum - minimum)
        )
    else:
        # Prevent division by zero when all values are equal
        df_cleaned[normalized_column] = 0.0

print("\nMin-Max normalization completed.")

# ==========================================================
# STEP 8: FINAL DATA QUALITY VALIDATION
# ==========================================================

if df_cleaned.empty:
    raise ValueError("The cleaned dataset is empty.")

if df_cleaned.isna().any().any():
    raise ValueError("Missing values remain in the cleaned dataset.")

if not (df_cleaned["delivery_time_minutes"] > 0).all():
    raise ValueError("Invalid delivery times remain.")

if not (df_cleaned["distance_km"] > 0).all():
    raise ValueError("Invalid distances remain.")

if not (df_cleaned["package_weight_kg"] > 0).all():
    raise ValueError("Invalid package weights remain.")

if not (df_cleaned["fuel_cost_usd"] > 0).all():
    raise ValueError("Invalid fuel costs remain.")

if not df_cleaned["traffic_index"].between(1, 5).all():
    raise ValueError("Invalid traffic index values remain.")

# Check normalized values are within [0, 1]
for column in normalization_columns:
    normalized_column = f"{column}_normalized"

    if not df_cleaned[normalized_column].between(0, 1).all():
        raise ValueError(
            f"Normalization validation failed for {normalized_column}."
        )

print("\nAll final data quality checks passed.")

# ==========================================================
# STEP 9: EXPORT CLEANED DATASET
# ==========================================================

cleaned_path = os.path.join(
    OUTPUT_DIR, "cleaned_logistics_data.csv"
)

df_cleaned.to_csv(cleaned_path, index=False)

print(f"\nCleaned dataset saved: {cleaned_path}")

# ==========================================================
# STEP 10: CREATE DELIVERY TIME DISTRIBUTION PLOT
# ==========================================================

plt.figure(figsize=(10, 5))

sns.histplot(
    data=df_cleaned,
    x="delivery_time_minutes",
    kde=True,
    bins=35,
)

plt.title(
    "Delivery Time Distribution After Cleaning",
    fontsize=13,
    fontweight="bold",
)
plt.xlabel("Delivery Time (Minutes)")
plt.ylabel("Number of Orders")
plt.tight_layout()

plot_path = os.path.join(
    OUTPUT_DIR, "delivery_time_distribution.png"
)

plt.savefig(plot_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Distribution plot saved: {plot_path}")

# ==========================================================
# STEP 11: CREATE DATA CLEANING SUMMARY
# ==========================================================

summary_rows = [
    ("Raw rows including duplicates", raw_row_count),
    ("Duplicate rows removed", duplicates_removed),
    ("Missing cells before cleaning", missing_before),
    ("Invalid delivery times detected", invalid_delivery_count),
    ("Invalid distances detected", invalid_distance_count),
    ("Invalid package weights detected", invalid_weight_count),
    ("Invalid fuel costs detected", invalid_fuel_count),
    ("Invalid traffic indexes detected", invalid_traffic_count),
    ("Delivery-time outliers removed", outliers_removed),
    ("Final cleaned rows", len(df_cleaned)),
    ("Final cleaned columns", len(df_cleaned.columns)),
    ("IQR lower limit", round(lower_limit, 2)),
    ("IQR upper limit", round(upper_limit, 2)),
]

for column, count in imputed_counts.items():
    summary_rows.append((f"Missing/invalid {column} values imputed", count))

summary_df = pd.DataFrame(
    summary_rows,
    columns=["metric", "value"]
)

summary_path = os.path.join(
    OUTPUT_DIR, "data_cleaning_summary.csv"
)

summary_df.to_csv(summary_path, index=False)

# ==========================================================
# STEP 12: PRINT FINAL SUMMARY
# ==========================================================

print("\n" + "=" * 65)
print("FINAL DATA CLEANING SUMMARY")
print("=" * 65)

print(f"Raw dataset rows: {raw_row_count}")
print(f"Final cleaned rows: {len(df_cleaned)}")
print(f"Rows removed as duplicates: {duplicates_removed}")
print(f"Delivery-time outliers removed: {outliers_removed}")
print(f"Missing cells after cleaning: {int(df_cleaned.isna().sum().sum())}")

print("\nCleaned dataset preview:")
print(df_cleaned.head())

print("\nGenerated files:")
print(f"- {raw_path}")
print(f"- {cleaned_path}")
print(f"- {plot_path}")
print(f"- {summary_path}")

print("\nWeek 2 logistics data preprocessing completed successfully.")
print("=" * 65)
