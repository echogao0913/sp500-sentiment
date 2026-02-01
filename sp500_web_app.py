#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S&P 500 Sentiment Analysis - Real-Time Web Dashboard
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from sp500_sentiment_analyzer import SP500SentimentAnalyzer
import sys
import io
import threading
import time
from datetime import datetime
import pandas as pd

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

def run_analysis():
    """Background task to run sentiment analysis"""
    global analysis_data

    with analysis_lock:
        analysis_data['status'] = 'running'
        analysis_data['progress'] = 0

    try:
        # Fetch company list
        analyzer.fetch_sp500_list()

        with analysis_lock:
            analysis_data['total_companies'] = len(analyzer.sp500_companies)

        # Analyze all companies
        analyzer.analyze_all_companies(sample_size=None)

        # Get predictions
        top_rises, top_falls = analyzer.get_predictions()

        # Convert to list of dicts
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

        print(f"Analysis completed at {analysis_data['last_update']}")

    except Exception as e:
        print(f"Error in analysis: {e}")
        with analysis_lock:
            analysis_data['status'] = 'error'
            analysis_data['error'] = str(e)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

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

    # Start analysis in background thread
    thread = threading.Thread(target=run_analysis)
    thread.daemon = True
    thread.start()

    return jsonify({'message': 'Analysis started'})

@app.route('/api/auto-refresh', methods=['POST'])
def toggle_auto_refresh():
    """Toggle auto-refresh mode"""
    data = request.get_json()
    enabled = data.get('enabled', False)
    interval = data.get('interval', 300)  # Default 5 minutes

    return jsonify({'enabled': enabled, 'interval': interval})

if __name__ == '__main__':
    import os

    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║           S&P 500 SENTIMENT ANALYSIS - WEB DASHBOARD STARTING               ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    print("Starting initial analysis...")
    # Run initial analysis
    run_analysis()

    print("\n" + "="*80)
    print("🌐 Web Dashboard is now running!")
    print("="*80)

    port = int(os.environ.get('PORT', 5000))

    if os.environ.get('RENDER'):
        print(f"\nRunning on Render cloud at port {port}")
    else:
        print("\nAccess the dashboard at:")
        print("  - Local: http://localhost:5000")
        print("  - Network: http://YOUR_IP_ADDRESS:5000")
        print("\nTo share with others on your network:")
        print("  1. Find your IP address (run: ipconfig)")
        print("  2. Share: http://YOUR_IP:5000")
        print("\nPress Ctrl+C to stop the server")

    print("="*80 + "\n")

    # Start Flask server
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
