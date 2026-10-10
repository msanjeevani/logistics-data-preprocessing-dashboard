
import os
import pandas as pd
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Logistics Preprocessing Dashboard</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f1f5f9;
    color: #172b4d;
}
nav {
    background: #102a43;
    color: white;
    padding: 20px 6%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}
nav h2 { margin: 0; }
nav span { color: #60a5fa; }
nav a {
    color: white;
    text-decoration: none;
    margin-left: 18px;
    font-size: 14px;
}
.container { max-width: 1200px; margin: auto; padding: 30px 20px; }
.hero {
    background: linear-gradient(120deg, #12344d, #2563eb);
    color: white;
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 25px;
}
.hero h1 { font-size: 32px; margin: 0 0 12px; }
.hero p { line-height: 1.7; color: #e0edff; }
.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 18px;
}
.card, .panel {
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 4px 15px #0f172a0b;
    margin-bottom: 20px;
}
.card p { color: #64748b; margin: 0 0 12px; }
.card h2 { font-size: 32px; margin: 0; color: #2563eb; }
.panel h2 { margin-top: 0; }
.links { display: flex; flex-wrap: wrap; gap: 12px; }
.btn {
    display: inline-block;
    background: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 14px;
}
.btn:hover { background: #1d4ed8; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td {
    padding: 12px;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
}
th { background: #eaf1fb; }
.table-wrap { overflow-x: auto; }
.chart { width: 100%; max-width: 900px; display: block; margin: auto; }
.notice {
    background: #fff7ed;
    color: #9a3412;
    padding: 14px;
    border-radius: 10px;
}
footer { text-align: center; color: #64748b; padding: 25px; }
@media(max-width: 600px) {
    .hero h1 { font-size: 25px; }
    .hero { padding: 25px; }
    nav a { margin-left: 0; margin-right: 10px; }
}
</style>
</head>
<body>
<nav>
  <h2>Logistics<span>Lab</span></h2>
  <div>
    <a href="/">Dashboard</a>
    <a href="/data/raw">Raw Data</a>
    <a href="/data/cleaned">Cleaned Data</a>
    <a href="/summary">Summary</a>
    <a href="/chart">Chart</a>
  </div>
</nav>

<div class="container">
  <section class="hero">
    <h1>Logistics Data Preprocessing</h1>
    <p>Week 2 Internship Project — Data Collection, Cleaning,
    Feature Engineering and Normalization.</p>
    <p>Dataset type: Synthetic / Simulated logistics data</p>
  </section>

  {% if error %}
    <div class="notice">{{ error }}</div>
  {% endif %}

  {% if page == 'dashboard' %}
    <div class="cards">
      <div class="card">
        <p>Raw Records</p><h2>{{ raw_count }}</h2>
      </div>
      <div class="card">
        <p>Cleaned Records</p><h2>{{ clean_count }}</h2>
      </div>
      <div class="card">
        <p>Duplicates Removed</p><h2>{{ duplicates }}</h2>
      </div>
      <div class="card">
        <p>Outliers Removed</p><h2>{{ outliers }}</h2>
      </div>
    </div>

    <section class="panel">
      <h2>Project Outputs</h2>
      <div class="links">
        <a class="btn" href="/data/raw">View Raw Dataset</a>
        <a class="btn" href="/data/cleaned">View Cleaned Dataset</a>
        <a class="btn" href="/summary">View Cleaning Summary</a>
        <a class="btn" href="/chart">View Delivery Chart</a>
      </div>
    </section>

    <section class="panel">
      <h2>Preprocessing Workflow</h2>
      <p>✓ Synthetic data generation</p>
      <p>✓ Duplicate detection and removal</p>
      <p>✓ Missing-value handling</p>
      <p>✓ Invalid-value validation</p>
      <p>✓ IQR outlier detection</p>
      <p>✓ Feature engineering and normalization</p>
    </section>

  {% elif page == 'table' %}
    <section class="panel">
      <h2>{{ title }}</h2>
      <p>Showing up to 100 rows.</p>
      {% if columns %}
      <div class="table-wrap">
        <table>
          <thead><tr>
            {% for col in columns %}<th>{{ col }}</th>{% endfor %}
          </tr></thead>
          <tbody>
          {% for row in rows %}
            <tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>
          {% endfor %}
          </tbody>
        </table>
      </div>
      {% else %}
        <p>No data available. Run preprocessing.py first.</p>
      {% endif %}
    </section>

  {% elif page == 'chart' %}
    <section class="panel">
      <h2>Delivery Time Distribution</h2>
      {% if chart_exists %}
        <img class="chart" src="/chart-image" alt="Delivery time histogram">
      {% else %}
        <p>Chart not found. Run preprocessing.py first.</p>
      {% endif %}
    </section>

  {% endif %}
</div>

<footer>LogisticsLab · Python · Pandas · Flask</footer>
</body>
</html>
"""


def read_csv(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        return None
    try:
        return pd.read_csv(path)
    except (OSError, ValueError, pd.errors.ParserError):
        return None


@app.route("/")
def dashboard():
    raw = read_csv("raw_logistics_data.csv")
    clean = read_csv("cleaned_logistics_data.csv")
    summary = read_csv("data_cleaning_summary.csv")

    raw_count = len(raw) if raw is not None else 0
    clean_count = len(clean) if clean is not None else 0
    duplicates = 0
    outliers = 0

    if summary is not None and {
        "Cleaning_Step", "Record_Count"
    }.issubset(summary.columns):
        counts = dict(zip(
            summary["Cleaning_Step"].astype(str),
            summary["Record_Count"]
        ))
        duplicates = int(counts.get(
            "Duplicate rows removed",
            counts.get("Duplicates Removed", 0)
        ))
        outliers = int(counts.get(
            "Delivery-time outliers removed (IQR)",
            counts.get("Outliers Removed (IQR)", 0)
        ))

    error = None
    if raw is None or clean is None:
        error = "Output files are missing. Run python preprocessing.py first."

    return render_template_string(
        HTML, page="dashboard", raw_count=raw_count,
        clean_count=clean_count, duplicates=duplicates,
        outliers=outliers, error=error
    )


@app.route("/data/<kind>")
def show_data(kind):
    files = {
        "raw": ("raw_logistics_data.csv", "Raw Logistics Dataset"),
        "cleaned": ("cleaned_logistics_data.csv", "Cleaned Logistics Dataset")
    }
    if kind not in files:
        return "Page not found", 404

    filename, title = files[kind]
    df = read_csv(filename)
    columns, rows = [], []

    if df is not None:
        preview = df.head(100).fillna("")
        columns = list(preview.columns)
        rows = preview.astype(str).values.tolist()

    return render_template_string(
        HTML, page="table", title=title, columns=columns,
        rows=rows, error=None
    )


@app.route("/summary")
def show_summary():
    df = read_csv("data_cleaning_summary.csv")
    columns, rows = [], []

    if df is not None:
        preview = df.fillna("")
        columns = list(preview.columns)
        rows = preview.astype(str).values.tolist()

    return render_template_string(
        HTML, page="table", title="Data Cleaning Summary",
        columns=columns, rows=rows, error=None
    )


@app.route("/chart")
def show_chart():
    chart_path = os.path.join(
        OUTPUT_DIR, "delivery_time_distribution.png"
    )
    return render_template_string(
        HTML, page="chart",
        chart_exists=os.path.exists(chart_path), error=None
    )


@app.route("/chart-image")
def chart_image():
    return send_from_directory(
        OUTPUT_DIR, "delivery_time_distribution.png"
    )


if __name__ == "__main__":
    print("Starting LogisticsLab dashboard...")
    print("Open this URL in your browser: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
