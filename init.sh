#!/bin/bash

set -e

# If you get a “Permission denied” error, make the script executable: 'chmod +x init.sh'

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔹 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
fi

# Activate virtual environment
echo "🔹 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated!"

# Install required packages
echo "🔹 Installing packages..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Packages installed!"

echo "✅ Setup complete! You can activate the virtual environment using 'source venv/bin/activate' and start project with 'uvicorn main:app --reload'"

