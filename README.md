
# Logistics Data Preprocessing Dashboard

A Python-based logistics data preprocessing project that generates synthetic logistics data, cleans and preprocesses the dataset, performs data quality checks, and visualizes delivery-time information through an interactive Flask web dashboard.

## Project Overview

This project demonstrates how raw logistics data can be transformed into clean, structured, and analysis-ready data using Python. It includes missing-value handling, duplicate removal, invalid-value detection, outlier removal, feature engineering, and Min-Max normalization.

The Flask dashboard allows users to view dataset statistics, explore raw and cleaned data, check the cleaning summary, and view the delivery-time distribution chart.

## Features

- Synthetic logistics dataset generation
- Missing-value detection and handling
- Duplicate record detection and removal
- Invalid delivery-time detection
- Outlier detection using the Interquartile Range (IQR) method
- Feature engineering
- Min-Max normalization
- Data quality validation
- Delivery-time distribution visualization
- Interactive Flask web dashboard
- CSV export for raw, cleaned, and summary data

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Flask
- HTML and CSS

## Project Structure

```text
logistics-data-preprocessing-dashboard/
│
├── app.py
├── preprocessing.py
├── requirements.txt
├── README.md
│
└── output/
    ├── raw_logistics_data.csv
    ├── cleaned_logistics_data.csv
    ├── delivery_time_distribution.png
    └── data_cleaning_summary.csv
```

## Data Preprocessing Workflow

1. Generate synthetic logistics data.
2. Inspect the raw dataset and identify missing values.
3. Detect and remove duplicate records.
4. Identify invalid delivery-time values.
5. Handle missing values.
6. Detect outliers using the IQR method.
7. Create additional features:
   - `avg_speed_kmh`
   - `cost_per_km`
8. Apply Min-Max normalization.
9. Validate the cleaned dataset.
10. Export the processed data and visualization files.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/logistics-data-preprocessing-dashboard.git
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Open the project folder

```bash
cd logistics-data-preprocessing-dashboard
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the Project

### Step 1: Run data preprocessing

```bash
python preprocessing.py
```

This generates the raw dataset, cleaned dataset, cleaning summary, and delivery-time chart inside the `output/` directory.

### Step 2: Start the Flask dashboard

```bash
python app.py
```

### Step 3: Open the dashboard

Open your browser and visit:

http://127.0.0.1:5000

Keep the terminal running while using the dashboard.

## Output Files

| File | Description |
|---|---|
| `raw_logistics_data.csv` | Original synthetic logistics dataset |
| `cleaned_logistics_data.csv` | Cleaned and processed dataset |
| `delivery_time_distribution.png` | Delivery-time distribution chart |
| `data_cleaning_summary.csv` | Data cleaning and quality summary |

## Results

In the current preprocessing run:

- Raw dataset: 1,520 rows
- Duplicate rows removed: 20
- Outlier rows removed: 20
- Final cleaned dataset: 1,480 rows
- Missing cells after cleaning: 0

These results describe the current generated dataset. They may change if the data-generation logic or random seed changes.

## Learning Outcomes

- Practical data cleaning using Pandas and NumPy
- Data quality assessment and validation
- Outlier detection using statistical methods
- Feature engineering and normalization
- Data visualization using Matplotlib and Seaborn
- Building a web dashboard using Flask
- Organizing a Python project for GitHub

## Future Enhancements

- Upload custom logistics CSV files
- Add interactive charts and filters
- Compare delivery performance across regions
- Analyze transportation costs and delivery delays
- Add downloadable cleaned datasets
- Deploy the dashboard online

## Disclaimer

This project uses synthetic data for educational and demonstration purposes. The results do not represent real-world logistics operations.

## Author

**Sanjee Vani M.**

B.E. Computer Science and Engineering Student

GitHub: https://github.com/msanjeevani

---

If you find this project useful, consider giving the repository a star!
