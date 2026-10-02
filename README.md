# Mama Earth Data Analytics Capstone Project

This repository contains the complete three-part data analytics pipeline for Mama Earth, covering SQL reporting, Python data cleaning/EDA, and a GenAI-powered insight narrator with an offline fallback path.

---

## Project Structure
- `sql/`: Contains database schema (`schema.sql`), seed data (`seed_data.sql`), and reporting queries (`reports.sql`).
- `data/`: Source CSV files (`orders.csv`, `customers.csv`, `products.csv`).
- `analysis/`: Python scripts for data cleaning, EDA (`clean_and_eda.py`), and visualization (`visualize.py`).
- `visualizations/`: Generated analytical charts (`return_rate_by_payment.png`, `monthly_revenue_trend.png`).
- `narrator/`: GenAI narrative script (`generate_narrative.py`), findings export (`findings.json`), and sample outputs (`sample_output.txt`).

---

# Mama Earth Data Analytics Capstone Project

This repository contains the complete three-part data analytics pipeline for Mama Earth, covering SQL reporting, Python data cleaning/EDA, and a GenAI-powered insight narrator with an offline fallback path.

---

## Project Structure
- `sql/`: Contains database schema (`schema.sql`), seed data (`seed_data.sql`), and reporting queries (`reports.sql`).
- `data/`: Source CSV files (`orders.csv`, `customers.csv`, `products.csv`).
- `analysis/`: Python scripts for data cleaning, EDA (`clean_and_eda.py`), and visualization (`visualize.py`).
- `visualizations/`: Generated analytical charts (`return_rate_by_payment.png`, `monthly_revenue_trend.png`).
- `narrator/`: GenAI narrative script (`generate_narrative.py`), findings export (`findings.json`), and sample outputs (`sample_output.txt`).

---

## Reproducibility Guide (Step-by-Step)

### SQL Setup & Reporting (Part 1)
Execute the SQL scripts sequentially in your SQLite/PostgreSQL environment:
1. Load schema: `sql/schema.sql`
2. Load seed data: `sql/seed_data.sql`
3. Run reporting queries: `sql/reports.sql`

### Python Data Wrangling & EDA (Part 2) & GenAI Narrator (Part 3)
Run the independent Python pipeline to clean data, handle anomalies, reconcile revenues, generate charts, and execute the automated narrative script:
```bash
python analysis/clean_and_eda.py
python analysis/visualize.py
python narrator/generate_narrative.py