import pandas as pd
import sys

SECTION_ORDER = ["Value", "Batting", "Fielding", "Running"]


def percentile_css(percentile: int):
    if percentile < 25:
        return "fill-low", "#1f77b4"
    elif percentile < 75:
        return "fill-mid", "#d3d3d3"
    else:
        return "fill-high", "#d62728"

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_percentiles.py <input_csv> <output_html>")
        sys.exit(1)

    input_csv, output_html = sys.argv[1], sys.argv[2]

    df = pd.read_csv(input_csv)

    required_cols = {"section", "metric_name", "raw_value", "percentile"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        print(f"Missing columns: {', '.join(missing)}")
        sys.exit(1)

    if "order" not in df.columns:
        df["order"] = range(1, len(df) + 1)

    df = df[df["section"].isin(SECTION_ORDER)].copy()
    df.sort_values(["section", "order"], inplace=True)

    # Build HTML
    css = """
    <style>
    * { margin:0; padding:0; box-sizing:border-box; font-family:sans-serif; }
    .container { width:800px; margin:40px auto 60px; }
    .header-title { font-size:28px; font-weight:bold; text-align:center; margin-bottom:8px; }
    .header-dots { text-align:center; font-size:24px; letter-spacing:24px; color:#008080; margin-bottom:24px; }
    .section { margin-bottom:32px; }
    .section-heading { display:flex; align-items:center; margin-bottom:4px; }
    .section-heading img { width:24px; height:24px; margin-right:8px; }
    .section-heading h2 { font-size:20px; font-weight:bold; color:#000; margin-right:8px; }
    .section-heading .underline { flex-grow:1; height:2px; background-color:#008080; }
    .value-guide { position:relative; width:600px; margin-left:200px; height:40px; margin-bottom:8px; }
    .value-guide .label { position:absolute; top:0; font-size:12px; font-weight:bold; }
    .value-guide .label-poor { left:calc(25% - 20px); color:#1f77b4; }
    .value-guide .label-avg  { left:calc(50% - 30px); color:#d3d3d3; }
    .value-guide .label-great{ left:calc(75% - 22px); color:#d62728; }
    .value-guide .triangle { position:absolute; top:16px; font-size:12px; line-height:12px; }
    .value-guide .tri-poor { left:calc(25% - 6px); color:#1f77b4; }
    .value-guide .tri-avg  { left:calc(50% - 6px); color:#d3d3d3; }
    .value-guide .tri-great{ left:calc(75% - 6px); color:#d62728; }
    .metric-row { display:flex; align-items:center; margin:4px 0; padding:8px 0; border-top:1px dashed #ccc; border-bottom:1px dashed #ccc; }
    .metric-name { width:200px; font-size:14px; color:#555; padding-left:4px; }
    .bar-container { position:relative; width:600px; height:16px; margin:0 16px; background-color:#ededed; border-radius:8px; overflow:hidden; }
    .bar-fill { height:100%; border-radius:8px 0 0 8px; }
    .fill-low  { background-color:#1f77b4; }
    .fill-mid  { background-color:#d3d3d3; }
    .fill-high { background-color:#d62728; }
    .percentile-badge { position:absolute; top:-4px; width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:bold; color:#fff; box-shadow:0 0 4px rgba(0,0,0,0.2); }
    .raw-value { width:80px; font-size:14px; color:#555; text-align:right; padding-right:4px; }
    .footer { margin-top:40px; font-size:12px; text-align:center; color:#888; }
    </style>
    """

    html_parts = ["<html><head>", css, "</head><body>", '<div class="container">']
    html_parts.append('<div class="header-title">2025 NCAA Percentile Rankings</div>')
    html_parts.append('<div class="header-dots">•   •   •   •   •</div>')

    icons = {
        "Value": "🏆",
        "Batting": "⚾",
        "Fielding": "🤾",
        "Running": "🏃",
    }

    for section in SECTION_ORDER:
        section_df = df[df["section"] == section]
        if section_df.empty:
            continue
        html_parts.append(f'<div class="section" id="section-{section.lower()}">')
        html_parts.append('<div class="section-heading">')
        icon = icons.get(section, "")
        html_parts.append(f'<img src="https://via.placeholder.com/24/000000/FFFFFF?text={icon}">')
        html_parts.append(f'<h2>{section}</h2>')
        html_parts.append('<div class="underline"></div>')
        html_parts.append('</div>')
        if section == "Value":
            html_parts.append('<div class="value-guide">')
            html_parts.append('<div class="label label-poor">POOR</div>')
            html_parts.append('<div class="label label-avg">AVERAGE</div>')
            html_parts.append('<div class="label label-great">GREAT</div>')
            html_parts.append('<div class="triangle tri-poor">▼</div>')
            html_parts.append('<div class="triangle tri-avg">▼</div>')
            html_parts.append('<div class="triangle tri-great">▼</div>')
            html_parts.append('</div>')
        for _, row in section_df.iterrows():
            fill_class, badge_color = percentile_css(int(row["percentile"]))
            pct = int(row["percentile"])
            html_parts.append('<div class="metric-row">')
            html_parts.append(f'<div class="metric-name">{row["metric_name"]}</div>')
            html_parts.append('<div class="bar-container">')
            html_parts.append(f'<div class="bar-fill {fill_class}" style="width: {pct}%;"></div>')
            html_parts.append(
                f'<div class="percentile-badge" style="left:calc({pct}% - 12px); background-color:{badge_color};">{pct}</div>'
            )
            html_parts.append('</div>')
            html_parts.append(f'<div class="raw-value">{row["raw_value"]}</div>')
            html_parts.append('</div>')
        html_parts.append('</div>')

    html_parts.append('<div class="footer">&bull; Generated by generate_percentiles.py &bull;</div>')
    html_parts.append('</div></body></html>')

    html = "".join(html_parts)
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Wrote HTML output to: {output_html}")

if __name__ == "__main__":
    main()
