# NCAA Trackman Percentile Rankings

Generate a static, Baseball Savant–style percentile rankings page from a CSV of NCAA Trackman metrics.

## Usage

1. Clone this repository.
2. Install [pandas](https://pandas.pydata.org/) (`pip install pandas`).
3. Run:
   ```bash
   python generate_percentiles.py data.csv index.html
   ```
4. Commit and push `index.html` to GitHub. Enable GitHub Pages in your repository settings to publish the page.

### Prerequisites

- Python >= 3.7
- pandas

### `data.csv` format

```
section,metric_name,raw_value,percentile,order
Value,Batting Run Value,10,89,1
Batting,xwOBA,0.380,87,1
Fielding,Range (OAA),0,46,1
Running,Sprint Speed,27.2,48,1
```

Add as many rows as needed. If the `order` column is omitted, rows retain their original CSV order.

Optional: configure a `CNAME` or adjust GitHub Pages settings if you want a custom domain.
