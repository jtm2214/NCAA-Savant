# NCAA Savant Percentile Rankings

This repository generates a static, Baseball Savant–style “Percentile Rankings” webpage from a CSV of NCAA Trackman metrics. The generated HTML can be hosted via GitHub Pages.

## Repository Structure

```
.
├── data.csv                # CSV file containing metrics and percentiles
├── generate_percentiles.py # Python script that reads data.csv and outputs index.html
├── requirements.txt        # Python dependencies (pandas)
├── setup.sh                # Script to create and activate virtual environment, and install dependencies
└── README.md               # This file
```

## Prerequisites

- Python 3.7 or higher
- `git`
- `pandas` (installed via `requirements.txt`)

## CSV Format

Your `data.csv` must include the following columns:

- `section`: One of `Value`, `Batting`, `Fielding`, or `Running`.
- `metric_name`: The label for the metric (e.g., `xwOBA`, `Bat Speed`).
- `raw_value`: The raw numeric or string value (e.g., `0.380`, `71.0`, `-1`, `86.3`).
- `percentile`: Integer between 0 and 100 representing the percentile rank.
- `order` (optional): Integer specifying row order within each section. If omitted, CSV row order is preserved.

Example `data.csv` snippet:

```csv
section,metric_name,raw_value,percentile,order
Value,Batting Run Value,10,89,1
Value,Baserunning Run Value,-1,14,2
Value,Fielding Run Value,0,51,3

Batting,xwOBA,0.380,87,1
Batting,xBA,0.261,50,2
Batting,xSLG,0.534,88,3
...
Fielding,Range (OAA),0,46,1
Fielding,Arm Value,0,59,2
Fielding,Arm Strength,86.3,66,3

Running,Sprint Speed,27.2,48,1
```

## Setup

1. Make the setup script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   This will:
   - Create a Python virtual environment in `./venv`
   - Activate the virtual environment
   - Install `pandas` from `requirements.txt`

2. If the script did not automatically activate the venv, run:
   ```bash
   source venv/bin/activate
   ```

## Generating the HTML

With the virtual environment activated:

```bash
python generate_percentiles.py data.csv index.html
```

- `data.csv`: Input CSV file.
- `index.html`: Output file containing the static webpage.

If successful, you’ll see:
```
✅ Wrote HTML output to: index.html
```

## Preview Locally

Open `index.html` in your browser to preview the Savant-style layout with your data:
```bash
open index.html    # macOS
xdg-open index.html  # Linux
```

## Deploy to GitHub Pages

1. Initialize git (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. Add remote:
   ```bash
   git remote add origin https://github.com/<your-username>/<repository>.git
   git branch -M main
   git push -u origin main
   ```
3. In your repository settings on GitHub, under **Pages**, select the `main` branch and `/ (root)` folder as the source. Save.
4. Your site will be published at:
   ```
   https://<your-username>.github.io/<repository>/
   ```

## Updating Data

Whenever you modify `data.csv`, re-run:

```bash
python generate_percentiles.py data.csv index.html
```

Then commit and push `index.html`:
```bash
git add index.html
git commit -m "Update percentiles"
git push
```

GitHub Pages will automatically reflect the changes.

---

© 2025 NCAA Savant Percentile Rankings
