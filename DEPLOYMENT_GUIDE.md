# Cloud Deployment Guide - S&P 500 Sentiment Dashboard

## ☁️ Deploy to Render (FREE - Recommended)

### Step 1: Create GitHub Repository

1. Go to https://github.com and login
2. Click "New Repository" (green button)
3. Repository name: `sp500-sentiment-dashboard`
4. Description: "Real-time S&P 500 stock sentiment analysis dashboard"
5. Choose "Public" (required for free Render deployment)
6. Click "Create repository"

### Step 2: Push Your Code to GitHub

Open Command Prompt in C:\Users\gaohanqi and run:

```bash
cd C:\Users\gaohanqi

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - S&P 500 Sentiment Dashboard"

# Add your GitHub repository (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/sp500-sentiment-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render

1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your `sp500-sentiment-dashboard` repository
5. Configure the service:
   - **Name:** sp500-sentiment-dashboard
   - **Region:** Choose closest to you
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn sp500_web_app:app --timeout 300 --workers 1`
   - **Instance Type:** Free
6. Click "Create Web Service"

### Step 4: Wait for Deployment

- Render will build and deploy (takes 5-10 minutes)
- You'll get a URL like: `https://sp500-sentiment-dashboard.onrender.com`
- Initial analysis will run automatically on first start

### Step 5: Share Your Dashboard

Share the URL with friends:
```
https://your-app-name.onrender.com
```

---

## 🚀 Alternative: Deploy to Railway (FREE)

### Step 1: Push to GitHub (Same as above)

### Step 2: Deploy to Railway

1. Go to https://railway.app and sign up (free)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `sp500-sentiment-dashboard` repository
5. Railway auto-detects Python and deploys
6. Click "Generate Domain" to get public URL

---

## 🐍 Alternative: Deploy to PythonAnywhere (FREE)

### Step 1: Sign Up

1. Go to https://www.pythonanywhere.com
2. Create free "Beginner" account

### Step 2: Upload Code

1. Go to "Files" tab
2. Upload all your Python files
3. Upload templates folder

### Step 3: Create Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask" framework
4. Point to `sp500_web_app.py`

### Step 4: Install Requirements

Open Bash console and run:
```bash
pip install --user -r requirements.txt
```

---

## 📋 Files You Need (Already Created)

✅ sp500_web_app.py - Main Flask application
✅ sp500_sentiment_analyzer.py - Analysis engine
✅ templates/dashboard.html - Web interface
✅ requirements.txt - Python dependencies
✅ Procfile - Deployment config
✅ runtime.txt - Python version
✅ README.md - Documentation
✅ .gitignore - Git ignore rules

---

## ⚠️ Important Notes

### Free Tier Limitations:

**Render:**
- App sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (more than enough)

**Railway:**
- $5 free credit per month
- Enough for ~500 hours of runtime

**PythonAnywhere:**
- Always-on
- Limited CPU/memory
- May be slower for analysis

### Recommendations:

1. **Best for sharing:** Render (easiest, reliable)
2. **Best performance:** Railway (faster)
3. **Always-on:** PythonAnywhere (no sleep)

---

## 🔧 Troubleshooting

### If deployment fails:

1. Check build logs in Render dashboard
2. Verify all files are in GitHub repository
3. Make sure requirements.txt has all dependencies
4. Try reducing workers in Procfile to 1

### If app is slow:

1. This is normal for free tier (cold starts)
2. First visit after sleep takes ~60 seconds
3. Subsequent visits are fast
4. Consider paid tier ($7/month) for always-on

---

## 📱 Next Steps After Deployment

1. Share your URL with friends
2. Enable auto-refresh on dashboard
3. Bookmark the URL on your phone
4. Set up custom domain (optional, paid)

---

## 💡 Pro Tips

- Visit your app daily to keep it warm
- Use UptimeRobot (free) to ping your app every 5 minutes (keeps it awake)
- Add Google Analytics to track visitors
- Share on social media!

---

## 🆘 Need Help?

If you encounter issues:
1. Check Render/Railway logs
2. Verify GitHub repository has all files
3. Test locally first: `python sp500_web_app.py`
4. Check that port 5000 works locally

---

Good luck with your deployment! 🚀
