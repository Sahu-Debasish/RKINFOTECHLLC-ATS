#!/bin/bash
# RK INFOTECH LLC — ATS Checker Setup Script
set -e

echo "======================================"
echo "  RK INFOTECH LLC ATS CHECKER SETUP"
echo "======================================"

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python: $(python3 --version)"

# Create virtual env
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
source venv/bin/activate

# Install deps
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

# Download NLTK data
echo "📚 Downloading NLTK data..."
python3 -c "
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)
print('✅ NLTK data ready')
"

# Create uploads dir
mkdir -p /tmp/ats_uploads

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🚀 Starting server at http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""

# Start Flask
python3 app.py
