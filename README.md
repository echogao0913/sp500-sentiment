# S&P 500 Sentiment Analysis Dashboard

Real-time stock sentiment predictions based on news analysis using VADER sentiment analysis.

## Features

- 📊 Analyzes 99 major S&P 500 companies
- 📈 Top 10 predicted rises (most bullish sentiment)
- 📉 Top 10 predicted falls (most bearish sentiment)
- 🔄 Auto-refresh every 5 minutes
- 🎨 Beautiful, modern UI with gradient design
- 📱 Mobile-responsive
- 🌐 Real-time news from Yahoo Finance RSS

## Live Demo

Visit: [Your Render URL will be here]

## How It Works

1. Fetches latest news headlines for each company via Yahoo Finance RSS feeds
2. Analyzes sentiment using VADER (Valence Aware Dictionary and sEntiment Reasoner)
3. Calculates prediction scores (-100 to +100)
4. Displays top 10 rises and falls in real-time dashboard

## Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python sp500_web_app.py

# Access at http://localhost:5000
```

## Deployment

This app is deployed on Render. See DEPLOYMENT_GUIDE.md for detailed instructions.

## Tech Stack

- **Backend:** Python, Flask
- **Sentiment Analysis:** VADER
- **Data Source:** Yahoo Finance RSS
- **Frontend:** HTML, CSS, JavaScript
- **Hosting:** Render (free tier)

## Disclaimer

⚠️ **This is for educational purposes only and NOT financial advice.**

Stock predictions are based solely on sentiment analysis and do not consider:
- Financial fundamentals
- Technical analysis
- Market conditions
- Economic factors

Always do your own research and consult with a qualified financial advisor before making investment decisions.

## License

MIT License

## Author

Built with Claude Code
