#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S&P 500 Sentiment Analysis - Web Dashboard (Standalone Version)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from sp500_sentiment_analyzer import SP500SentimentAnalyzer
import sys
import io
import threading
import time
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Global variables
analyzer = SP500SentimentAnalyzer()
analysis_data = {
    'top_rises': [],
    'top_falls': [],
    'last_update': None,
    'status': 'idle',
    'progress': 0,
    'total_companies': 0
}
analysis_lock = threading.Lock()

# Embedded HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
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
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        .status { display: flex; align-items: center; gap: 10px; }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4caf50;
            animation: pulse 2s infinite;
        }
        .status-indicator.running { background: #ff9800; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: all 0.3s;
        }
        button:hover { background: #5568d3; transform: translateY(-2px); }
        button:disabled { background: #ccc; cursor: not-allowed; }
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
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .stock-item:hover { transform: translateX(5px); }
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
        .loading { text-align: center; padding: 40px; color: #666; }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
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
            <div class="status">
                <div class="status-indicator" id="statusIndicator"></div>
                <span id="statusText">Loading...</span>
                <span id="lastUpdate"></span>
            </div>
            <button id="refreshBtn" onclick="refreshData()">🔄 Refresh Now</button>
        </div>

        <div id="loadingMsg" class="loading">
            <div class="spinner"></div>
            <p>Analyzing 99 S&P 500 companies... This may take a few minutes.</p>
        </div>

        <div class="grid" id="dataGrid" style="display: none;">
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
        async function fetchData() {
            try {
                const response = await fetch('/api/data');
                const data = await response.json();

                const indicator = document.getElementById('statusIndicator');
                const statusText = document.getElementById('statusText');
                const lastUpdate = document.getElementById('lastUpdate');

                indicator.className = 'status-indicator ' + data.status;
                statusText.textContent = data.status === 'completed' ? 'Up to date' : 'Analyzing...';
                if (data.last_update) lastUpdate.textContent = 'Last: ' + data.last_update;

                if (data.top_rises && data.top_rises.length > 0) {
                    document.getElementById('loadingMsg').style.display = 'none';
                    document.getElementById('dataGrid').style.display = 'grid';
                    updateStockList('topRises', data.top_rises, 'rise');
                    updateStockList('topFalls', data.top_falls, 'fall');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }

        function updateStockList(elementId, stocks, type) {
            const container = document.getElementById(elementId);
            container.innerHTML = '';

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
                    <div class="stock-headline">"${stock.headline.substring(0, 80)}..."</div>
                `;
                container.appendChild(item);
            });
        }

        async function refreshData() {
            const btn = document.getElementById('refreshBtn');
            btn.disabled = true;
            btn.textContent = '⏳ Analyzing...';
            document.getElementById('loadingMsg').style.display = 'block';
            document.getElementById('dataGrid').style.display = 'none';

            await fetch('/api/refresh', { method: 'POST' });

            const pollInterval = setInterval(async () => {
                const response = await fetch('/api/data');
                const data = await response.json();
                if (data.status === 'completed') {
                    clearInterval(pollInterval);
                    btn.disabled = false;
                    btn.textContent = '🔄 Refresh Now';
                    fetchData();
                }
            }, 3000);
        }

        fetchData();
        setInterval(fetchData, 10000);
    </script>
</body>
</html>
"""

def run_analysis():
    """Background task to run sentiment analysis"""
    global analysis_data

    with analysis_lock:
        analysis_data['status'] = 'running'
        analysis_data['progress'] = 0

    try:
        analyzer.fetch_sp500_list()

        with analysis_lock:
            analysis_data['total_companies'] = len(analyzer.sp500_companies)

        analyzer.analyze_all_companies(sample_size=None)
        top_rises, top_falls = analyzer.get_predictions()

        rises_list = []
        for idx, row in enumerate(top_rises.itertuples(), 1):
            rises_list.append({
                'rank': idx,
                'ticker': row.ticker,
                'company': row.company,
                'score': round(row.prediction_score, 2),
                'sentiment': round(row.sentiment_compound, 3),
                'headline': row.sample_headlines[0] if row.sample_headlines else ''
            })

        falls_list = []
        for idx, row in enumerate(top_falls.itertuples(), 1):
            falls_list.append({
                'rank': idx,
                'ticker': row.ticker,
                'company': row.company,
                'score': round(row.prediction_score, 2),
                'sentiment': round(row.sentiment_compound, 3),
                'headline': row.sample_headlines[0] if row.sample_headlines else ''
            })

        with analysis_lock:
            analysis_data['top_rises'] = rises_list
            analysis_data['top_falls'] = falls_list
            analysis_data['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            analysis_data['status'] = 'completed'
            analysis_data['progress'] = 100

    except Exception as e:
        print(f"Error in analysis: {e}")
        with analysis_lock:
            analysis_data['status'] = 'error'

@app.route('/')
def index():
    """Main dashboard page"""
    return HTML_TEMPLATE

@app.route('/api/data')
def get_data():
    """API endpoint to get current analysis data"""
    with analysis_lock:
        return jsonify(analysis_data)

@app.route('/api/refresh', methods=['POST'])
def refresh_analysis():
    """API endpoint to trigger new analysis"""
    with analysis_lock:
        if analysis_data['status'] == 'running':
            return jsonify({'error': 'Analysis already running'}), 400

    thread = threading.Thread(target=run_analysis)
    thread.daemon = True
    thread.start()

    return jsonify({'message': 'Analysis started'})

if __name__ == '__main__':
    import os

    port = int(os.environ.get('PORT', 5000))
    print(f"\nWeb Dashboard running on port {port}")

    # Start analysis in background thread (don't block startup)
    thread = threading.Thread(target=run_analysis)
    thread.daemon = True
    thread.start()

    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
