#!/bin/bash

echo "🔐 Starting Secure Mega Dashboard Server"
echo "========================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed"
    exit 1
fi

# Install requirements if not already installed
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt --quiet

# Start the server
echo "✅ Dependencies installed"
echo ""
python3 server.py

