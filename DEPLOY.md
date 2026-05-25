# 🚀 RK INFOTECH LLC — ATS Checker Deployment Guide

## Option 1: Run Locally (Quickest)

```bash
# 1. Install Python 3.9+ if not installed

# 2. Run setup script
chmod +x start.sh
./start.sh

# 3. Open browser → http://localhost:5000
```

---

## Option 2: Deploy on Render.com (FREE — Recommended)

1. Push code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "RK Infotech ATS Checker"
   git remote add origin https://github.com/YOUR_USERNAME/ats-checker.git
   git push -u origin main
   ```

2. Go to https://render.com → Sign up (free)

3. Click **"New Web Service"** → Connect GitHub repo

4. Settings:
   - **Name**: rk-infotech-ats-checker
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('punkt_tab', quiet=True)"`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan**: Free

5. Click **Deploy** → Wait 3-5 min → Your site is live! 🎉

---

## Option 3: Deploy on Railway.app (Easy)

1. Go to https://railway.app → Sign up with GitHub
2. Click **"New Project"** → **"Deploy from GitHub"**
3. Select your repo → Railway auto-detects Python + Procfile
4. Click **"Deploy"** → Done!

---

## Option 4: Deploy on Heroku

```bash
# Install Heroku CLI first
heroku create rk-infotech-ats-checker
heroku buildpacks:set heroku/python
git push heroku main
heroku open
```

---

## Option 5: Deploy with Docker

```bash
# Build
docker build -t ats-checker .

# Run
docker run -p 5000:5000 ats-checker

# Open http://localhost:5000
```

---

## Option 6: Deploy on a VPS (DigitalOcean/AWS/Hetzner)

```bash
# SSH into your server
ssh user@your-server-ip

# Install Python & Nginx
sudo apt update
sudo apt install python3 python3-pip nginx -y

# Clone/upload your code
# Then run:
pip3 install -r requirements.txt
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# Install gunicorn
pip3 install gunicorn

# Run with gunicorn
gunicorn app:app --bind 127.0.0.1:5000 --workers 2 --daemon

# Configure Nginx (create /etc/nginx/sites-available/ats):
# server {
#     listen 80;
#     server_name your-domain.com;
#     location / {
#         proxy_pass http://127.0.0.1:5000;
#         proxy_set_header Host $host;
#     }
# }
sudo nginx -t && sudo systemctl reload nginx
```

---

## File Structure

```
ats-checker/
├── app.py              ← Main Flask backend (ATS engine)
├── requirements.txt    ← Python dependencies
├── Procfile           ← For Heroku/Render
├── Dockerfile         ← For Docker deployment
├── start.sh           ← Local setup script
├── DEPLOY.md          ← This file
├── templates/
│   └── index.html     ← Full frontend UI
└── static/
    ├── assets/
    │   └── logo.png   ← RK Infotech LLC logo
    ├── css/           ← (optional extra CSS)
    └── js/            ← (optional extra JS)
```

---

## Features

- ✅ Upload PDF, DOCX, DOC, TXT resumes
- ✅ Overall ATS score (0-100)
- ✅ 14+ job roles with 500+ keywords
- ✅ Job Description matching
- ✅ Contact info detection
- ✅ Section analysis
- ✅ Action verb scoring
- ✅ Quantification scoring
- ✅ Formatting issue detection
- ✅ Download report as TXT
- ✅ Mobile responsive

---

© 2025 RK INFOTECH LLC — THE FUTURE BLOOMS IN CODE
