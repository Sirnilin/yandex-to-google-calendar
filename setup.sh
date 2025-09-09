#!/bin/bash

# Setup script for Yandex to Google Calendar Sync

set -e

echo "🚀 Setting up Yandex to Google Calendar Sync"
echo "================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.11 or later and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs

# Copy environment template
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file from template"
        echo "⚠️  Please edit .env file with your credentials"
    else
        echo "❌ .env.example file not found"
        exit 1
    fi
else
    echo "ℹ️  .env file already exists"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    echo "❌ pip not found. Please install pip and try again."
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Check for credentials file
if [ ! -f "data/credentials.json" ]; then
    echo "⚠️  Google credentials file not found at data/credentials.json"
    echo "📋 Please follow these steps:"
    echo "   1. Go to https://console.cloud.google.com/"
    echo "   2. Create a new project or select existing one"
    echo "   3. Enable Google Calendar API"
    echo "   4. Create OAuth 2.0 credentials (Desktop Application)"
    echo "   5. Download the JSON file and save as data/credentials.json"
fi

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Yandex credentials"
echo "2. Download Google credentials.json to data/ folder"
echo "3. Run: python main.py once (for single sync)"
echo "4. Run: python main.py continuous (for ongoing sync)"
echo ""
echo "For Docker deployment:"
echo "1. Complete steps above"
echo "2. Run: docker-compose up -d"
echo ""
echo "Need help? Check the README.md file for detailed instructions."