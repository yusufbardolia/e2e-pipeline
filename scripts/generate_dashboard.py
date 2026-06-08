
import json
import os
from datetime import datetime

def generate_html_report(test_results, output_filename):
    # Calculate summary metrics
    total_tests = len(test_results)
    passed_tests = sum(1 for test in test_results if test['status'] == 'Pass')
    failed_tests = total_tests - passed_tests
    
    # Generate table rows dynamically
    table_rows = ""
    for test in test_results:
        status_color = "#2ecc71" if test['status'] == 'Pass' else "#e74c3c"
        table_rows += f"""
        <tr>
            <td style="font-family: monospace;">{test['name']}</td>
            <td style="color: {status_color}; font-weight: bold;">{test['status']}</td>
            <td>{test['duration']}s</td>
        </tr>
        """

    # HTML Template with embedded CSS and Chart.js
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Elea.ai - AI Test Pipeline Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 40px; color: #333; }}
            .container {{ max-width: 900px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }}
            h1 {{ text-align: center; color: #2c3e50; margin-bottom: 5px; }}
            .timestamp {{ text-align: center; color: #7f8c8d; font-size: 0.9em; margin-bottom: 40px; }}
            .summary-cards {{ display: flex; justify-content: space-between; margin-bottom: 40px; gap: 20px; }}
            .card {{ flex: 1; text-align: center; padding: 25px; border-radius: 10px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .card.total {{ background-color: #34495e; }}
            .card.passed {{ background-color: #2ecc71; }}
            .card.failed {{ background-color: #e74c3c; }}
            .card h3 {{ margin: 0 0 10px 0; font-size: 1.1em; font-weight: 400; opacity: 0.9; }}
            .card h2 {{ margin: 0; font-size: 2.5em; }}
            .data-section {{ display: flex; gap: 40px; align-items: center; }}
            .chart-container {{ flex: 1; max-width: 300px; }}
            .table-container {{ flex: 2; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #ecf0f1; }}
            th {{ background-color: #f8f9fa; color: #7f8c8d; font-weight: 600; text-transform: uppercase; font-size: 0.85em; letter-spacing: 0.5px; }}
            tr:hover {{ background-color: #fdfdfd; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 E2E Testing Gateway</h1>
            <div class="timestamp">Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
            
            <div class="summary-cards">
                <div class="card total">
                    <h3>Total Scenarios</h3>
                    <h2>{total_tests}</h2>
                </div>
                <div class="card passed">
                    <h3>Passed</h3>
                    <h2>{passed_tests}</h2>
                </div>
                <div class="card failed">
                    <h3>Failed</h3>
                    <h2>{failed_tests}</h2>
                </div>
            </div>

            <div class="data-section">
                <div class="chart-container">
                    <canvas id="resultsChart"></canvas>
                </div>
                
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Generated Test Flow</th>
                                <th>Status</th>
                                <th>Execution Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <script>
            const ctx = document.getElementById('resultsChart').getContext('2d');
            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['Passed', 'Failed'],
                    datasets: [{{
                        data: [{passed_tests}, {failed_tests}],
                        backgroundColor: ['#2ecc71', '#e74c3c'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    cutout: '70%',
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ padding: 20, font: {{ family: "'Segoe UI', sans-serif" }} }} }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Visual Dashboard successfully generated at: {output_filename}")

if __name__ == "__main__":
    # Mock data representing what Maestro would output in a real environment
    sample_results = [
        {"name": "BUG-101_flow.yaml", "status": "Pass", "duration": 4.2},
        {"name": "LOGIN_flow.yaml", "status": "Pass", "duration": 3.8},
        {"name": "CHECKOUT_flow.yaml", "status": "Fail", "duration": 12.1},
        {"name": "PROFILE_flow.yaml", "status": "Pass", "duration": 2.5}
    ]
    
    generate_html_report(sample_results, "tests/dashboard.html")
