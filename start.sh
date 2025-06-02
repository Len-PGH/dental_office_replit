#!/bin/bash

echo "🦷 SignalWire Dental Office Management System"
echo "================================"
echo

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo "Please run: python setup.py"
    echo
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements if needed
echo "📋 Checking dependencies..."
pip install -r requirements.txt --quiet

# Start the application
echo "🚀 Starting SignalWire Dental Office Management System..."
echo
echo "🌐 Application will be available at:"
echo "   http://127.0.0.1:8080"
echo
echo "👥 Default Login Credentials:"
echo "   Patient: jane.doe@email.com / patient123"
echo "   Dentist: dr.smith@dentaloffice.com / dentist123"
echo
echo "Press Ctrl+C to stop the server"
echo

python app.py 