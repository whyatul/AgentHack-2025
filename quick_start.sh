#!/bin/bash

# AI Meme Stock Predictor - Quick Start Script
# This script helps you get the project running quickly

set -e  # Exit on any error

echo "🚀 AI Meme Stock Predictor - Quick Start"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "cli.py" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Step 1: Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1)
print_status "Found: $python_version"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    print_error "Python 3.8+ required. Please upgrade Python."
    exit 1
fi

# Step 2: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
else
    print_status "Virtual environment already exists"
fi

# Step 3: Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Step 4: Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Step 5: Install core dependencies
print_status "Installing core dependencies..."
pip install fastapi uvicorn pydantic requests python-dotenv

# Step 6: Install analysis dependencies
print_status "Installing analysis dependencies..."
pip install vaderSentiment

# Step 7: Install data source dependencies
print_status "Installing data source dependencies..."
pip install praw tweepy

# Step 8: Install Telegram bot dependency
print_status "Installing Telegram bot dependency..."
pip install python-telegram-bot

# Step 9: Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please edit .env file and add your API keys!"
else
    print_status ".env file already exists"
fi

# Step 10: Run verification script
print_status "Running project verification..."
if python verify_setup.py; then
    echo ""
    print_status "✅ Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file and add your API keys"
    echo "2. Test CLI: python cli.py TSLA"
    echo "3. Start web server: uvicorn src.ai_meme_stock_predictor.web.app:app --reload"
    echo "4. Visit http://127.0.0.1:8000/docs for API documentation"
    echo ""
else
    print_error "Setup verification failed. Please check the output above."
    exit 1
fi

echo "🎉 Ready to predict meme stocks!"
