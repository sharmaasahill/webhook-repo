#!/bin/bash

# TechStax Assessment - Setup Script
# This script helps you quickly set up the webhook receiver application

set -e

echo "🚀 TechStax Assessment - Webhook Receiver Setup"
echo "==============================================="
echo

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or higher."
    exit 1
fi

python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✅ pip is available"

# Check if MongoDB is running
if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB is not installed or not in PATH."
    echo "   Please install MongoDB and make sure it's running."
    echo "   You can also use MongoDB Atlas cloud service."
else
    echo "✅ MongoDB is available"
fi

# Create virtual environment
echo
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo
echo "🔄 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows Git Bash
    source venv/Scripts/activate
else
    # macOS/Linux
    source venv/bin/activate
fi

echo "✅ Virtual environment activated"

# Install dependencies
echo
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Setup environment file
echo
echo "⚙️  Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp env.example .env
    echo "✅ Environment file created (.env)"
    echo "ℹ️  Please edit .env file with your configuration:"
    echo "   - Set your MongoDB URI"  
    echo "   - Set your GitHub webhook secret"
else
    echo "✅ Environment file already exists"
fi

# Check if ngrok is available
echo
if command -v ngrok &> /dev/null; then
    echo "✅ ngrok is available for webhook testing"
else
    echo "⚠️  ngrok is not installed."
    echo "   Install ngrok from https://ngrok.com to test webhooks locally"
fi

echo
echo "🎉 Setup completed!"
echo
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Make sure MongoDB is running"
echo "3. Run: python app.py"
echo "4. In another terminal, run: ngrok http 5000"
echo "5. Configure GitHub webhook with ngrok URL"
echo
echo "Visit http://localhost:5000 to see the web interface"
echo

deactivate 2>/dev/null || true 