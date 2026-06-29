import json
from datetime import datetime

def generate_html(enriched_data):
    rows = ""
    for item in enriched_data:
        verdict = item.get("verdict", "")
        if "MALICIOUS" in verdict:
            color = "#ff4d4d"
            icon = "🔴"
        elif "NOT FOUND" in verdict:
            color = "#ffd700"
            icon = "❓"
        else:
            color = "#34d399"
            icon = "🟢"

        rows += f"""
        <tr>
            <td>{item.get('type','')}</td>
            <td style='word-break:break-all;font-family:monospace;font-size:13px'>{item.get('ioc','')}</td>
            <td style='color:#ff4d4d;font-weight:700'>{item.get('malicious','N/A')}</td>
            <td style='color:#ffd700'>{item.get('suspicious','N/A')}</td>
            <td style='color:{color};font-weight:700'>{icon} {verdict}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>IOC Threat Intelligence Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #0b1020;
            color: #e8eefc;
            padding: 40px;
        }}
        h1 {{ color: #7dd3fc; font-size: 28px; }}
        .meta {{ color: #b7c3df; margin-bottom: 30px; font-size: 14px; }}
        .summary {{
            display: flex; gap: 20px; margin-bottom: 30px;
        }}
        .stat {{
            background: #111a33;
            border: 1px solid #263252;
            border-radius: 12px;
            padding: 16px 24px;
            text-align: center;
        }}
        .stat strong {{ display: block; font-size: 28px; color: #ff4d4d; }}
        .stat span {{ color: #b7c3df; font-size: 13px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th {{
            background: #16223f;
            padding: 12px;
            text-align: left;
            color: #7dd3fc;
            border: 1px solid #263252;
        }}
        td {{
            border: 1px solid #263252;
            padding: 10px 12px;
        }}
        tr:hover {{ background: #111a33; }}
    </style>
</head>
<body>
    <h1>🔎 IOC Threat Intelligence Report</h1>
    <div class="meta">
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Source: Akira Ransomware — Unit42 / Palo Alto Networks</p>
        <p>Total IOCs Analyzed: <strong>{len(enriched_data)}</strong></p>
    </div>

    <div class="summary">
        <div class="stat">
            <strong>{sum(1 for i in enriched_data if 'MALICIOUS' in i.get('verdict',''))}</strong>
            <span>Malicious</span>
        </div>
        <div class="stat">
            <strong style="color:#ffd700">{sum(1 for i in enriched_data if 'NOT FOUND' in i.get('verdict',''))}</strong>
            <span>Not Found</span>
        </div>
        <div class="stat">
            <strong style="color:#34d399">{sum(1 for i in enriched_data if 'CLEAN' in i.get('verdict',''))}</strong>
            <span>Clean</span>
        </div>
    </div>

    <table>
        <tr>
            <th>Type</th>
            <th>IOC</th>
            <th>Malicious Detections</th>
            <th>Suspicious</th>
            <th>Verdict</th>
        </tr>
        {rows}
    </table>
</body>
</html>"""

    with open("ioc_report.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[+] Report saved as ioc_report.html")
    print("[+] Open ioc_report.html in your browser to view it")


if __name__ == "__main__":
    with open("iocs_enriched.json") as f:
        data = json.load(f)
    generate_html(data)