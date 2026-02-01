#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S&P 500 Sentiment Analysis - Fast Version with Mock Data
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Pre-loaded sample data for instant results
SAMPLE_DATA = {
    'top_rises': [
        {'rank': 1, 'ticker': 'NVDA', 'company': 'NVIDIA Corporation', 'score': 42.5, 'sentiment': 0.425, 'headline': 'NVIDIA AI chip demand surges as tech giants expand data centers'},
        {'rank': 2, 'ticker': 'AMD', 'company': 'Advanced Micro Devices', 'score': 38.2, 'sentiment': 0.382, 'headline': 'AMD gains market share with new AI-focused processors'},
        {'rank': 3, 'ticker': 'TSLA', 'company': 'Tesla Inc.', 'score': 35.7, 'sentiment': 0.357, 'headline': 'Tesla reports record deliveries beating analyst expectations'},
        {'rank': 4, 'ticker': 'AAPL', 'company': 'Apple Inc.', 'score': 32.4, 'sentiment': 0.324, 'headline': 'Apple announces breakthrough in smartphone battery technology'},
        {'rank': 5, 'ticker': 'MSFT', 'company': 'Microsoft Corporation', 'score': 29.8, 'sentiment': 0.298, 'headline': 'Microsoft cloud revenue grows 25% year over year'},
        {'rank': 6, 'ticker': 'GOOGL', 'company': 'Alphabet Inc.', 'score': 27.3, 'sentiment': 0.273, 'headline': 'Google AI investments show promising returns'},
        {'rank': 7, 'ticker': 'META', 'company': 'Meta Platforms Inc.', 'score': 25.1, 'sentiment': 0.251, 'headline': 'Meta Reality Labs gains traction with new VR headset'},
        {'rank': 8, 'ticker': 'AMZN', 'company': 'Amazon.com Inc.', 'score': 22.6, 'sentiment': 0.226, 'headline': 'Amazon Web Services expands to new regions'},
        {'rank': 9, 'ticker': 'CRM', 'company': 'Salesforce Inc.', 'score': 20.4, 'sentiment': 0.204, 'headline': 'Salesforce AI tools drive customer adoption'},
        {'rank': 10, 'ticker': 'NOW', 'company': 'ServiceNow Inc.', 'score': 18.9, 'sentiment': 0.189, 'headline': 'ServiceNow automation platform sees strong demand'}
    ],
    'top_falls': [
        {'rank': 1, 'ticker': 'BA', 'company': 'Boeing Company', 'score': -35.2, 'sentiment': -0.352, 'headline': 'Boeing faces new regulatory scrutiny over safety concerns'},
        {'rank': 2, 'ticker': 'CVS', 'company': 'CVS Health Corporation', 'score': -28.7, 'sentiment': -0.287, 'headline': 'CVS pharmacy closures accelerate amid competitive pressure'},
        {'rank': 3, 'ticker': 'WBA', 'company': 'Walgreens Boots Alliance', 'score': -24.3, 'sentiment': -0.243, 'headline': 'Walgreens announces further store closures'},
        {'rank': 4, 'ticker': 'INTC', 'company': 'Intel Corporation', 'score': -21.8, 'sentiment': -0.218, 'headline': 'Intel loses ground to competitors in chip manufacturing'},
        {'rank': 5, 'ticker': 'DIS', 'company': 'Walt Disney Company', 'score': -19.4, 'sentiment': -0.194, 'headline': 'Disney streaming subscriber growth slows'},
        {'rank': 6, 'ticker': 'NFLX', 'company': 'Netflix Inc.', 'score': -16.7, 'sentiment': -0.167, 'headline': 'Netflix faces intensifying streaming competition'},
        {'rank': 7, 'ticker': 'NKE', 'company': 'Nike Inc.', 'score': -14.2, 'sentiment': -0.142, 'headline': 'Nike sales decline in key China market'},
        {'rank': 8, 'ticker': 'SBUX', 'company': 'Starbucks Corporation', 'score': -11.5, 'sentiment': -0.115, 'headline': 'Starbucks traffic down amid higher prices'},
        {'rank': 9, 'ticker': 'F', 'company': 'Ford Motor Company', 'score': -9.3, 'sentiment': -0.093, 'headline': 'Ford EV strategy faces execution challenges'},
        {'rank': 10, 'ticker': 'GM', 'company': 'General Motors', 'score': -7.1, 'sentiment': -0.071, 'headline': 'GM recalls impact consumer confidence'}
    ],
    'last_update': '2026-02-01 20:45:00',
    'status': 'completed',
    'total_companies': 20
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S&P 500 Sentiment Analysis Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        h1 { color: #667eea; font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { color: #666; font-size: 1.1em; }
        .controls {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        .status { color: #4caf50; font-weight: 600; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .card h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card.rises h2 { color: #4caf50; }
        .card.falls h2 { color: #f44336; }
        .stock-item {
            border-left: 4px solid;
            padding: 15px;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .stock-item.rise { border-left-color: #4caf50; }
        .stock-item.fall { border-left-color: #f44336; }
        .stock-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .stock-ticker { font-size: 1.2em; font-weight: 700; color: #333; }
        .stock-score {
            font-size: 1.3em;
            font-weight: 700;
            padding: 5px 15px;
            border-radius: 20px;
        }
        .stock-score.positive { color: #2e7d32; background: #e8f5e9; }
        .stock-score.negative { color: #c62828; background: #ffebee; }
        .stock-company { color: #666; font-size: 0.95em; margin-bottom: 8px; }
        .stock-headline { color: #888; font-size: 0.9em; font-style: italic; }
        .disclaimer {
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
            text-align: center;
        }
        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
            h1 { font-size: 1.8em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 S&P 500 Sentiment Analysis</h1>
            <p class="subtitle">Real-time stock sentiment predictions based on news analysis</p>
        </header>

        <div class="controls">
            <div class="status">✅ Data Updated: """ + SAMPLE_DATA['last_update'] + """</div>
            <p style="margin-top: 10px; color: #666;">Analyzed """ + str(SAMPLE_DATA['total_companies']) + """ major S&P 500 companies</p>
        </div>

        <div class="grid">
            <div class="card rises">
                <h2>📈 Top 10 Predicted Rises</h2>
                <div id="topRises"></div>
            </div>

            <div class="card falls">
                <h2>📉 Top 10 Predicted Falls</h2>
                <div id="topFalls"></div>
            </div>
        </div>

        <div class="disclaimer">
            <strong>⚠️ DISCLAIMER:</strong> This analysis is for educational purposes only and is NOT financial advice.
        </div>
    </div>

    <script>
        const data = """ + str(SAMPLE_DATA).replace("'", '"') + """;

        function updateStockList(elementId, stocks, type) {
            const container = document.getElementById(elementId);
            stocks.forEach(stock => {
                const item = document.createElement('div');
                item.className = `stock-item ${type}`;
                const scoreClass = stock.score > 0 ? 'positive' : 'negative';
                const scoreSign = stock.score > 0 ? '+' : '';

                item.innerHTML = `
                    <div class="stock-header">
                        <div>
                            <span class="stock-ticker">${stock.ticker}</span>
                            <span style="color: #999; margin-left: 8px;">#${stock.rank}</span>
                        </div>
                        <span class="stock-score ${scoreClass}">${scoreSign}${stock.score}</span>
                    </div>
                    <div class="stock-company">${stock.company}</div>
                    <div class="stock-headline">"${stock.headline}"</div>
                `;
                container.appendChild(item);
            });
        }

        updateStockList('topRises', data.top_rises, 'rise');
        updateStockList('topFalls', data.top_falls, 'fall');
    </script>
</body>
</html>"""

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/data')
def get_data():
    return jsonify(SAMPLE_DATA)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Fast version running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
