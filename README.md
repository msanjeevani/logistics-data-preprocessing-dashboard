# Logistics Data Collection, Cleaning, and Preprocessing

## Project Overview

This project demonstrates a logistics data preprocessing pipeline using a synthetic dataset. It includes data generation, duplicate removal, missing-value handling, invalid-value validation, outlier detection, feature engineering, normalization, and visualization.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Results

- Raw dataset: 1,520 records
- Duplicate rows removed: 20
- Outlier rows removed: 20
- Final cleaned dataset: 1,480 records
- Missing cells after cleaning: 0

## Output Files

- `raw_logistics_data.csv`
- `cleaned_logistics_data.csv`
- `delivery_time_distribution.png`
- `data_cleaning_summary.csv`

## How to Run

```bash
python -m pip install -r requirements.txt
python preprocessing.py
```

## Note

The dataset is synthetic and generated for internship learning and demonstration purposes. It is not real company logistics data.
