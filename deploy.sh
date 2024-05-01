#!/bin/bash

# get python interpreter
PYTHON=$(command -v python3 || command -v python)

# check if python is found
if [ -z "$PYTHON" ]; then
    echo "Python interpreter not found. Please install Python."
    exit 1
fi

# create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv .venv
fi

# activate virtual environment
source .venv/bin/activate

if [ ! -f ".venv/bin/flask" ]; then
    echo "Installing dependencies..."
    pip install Flask > /dev/null 2>&1
    pip install google-generativeai > /dev/null 2>&1
    pip install beautifulsoup4 > /dev/null 2>&1
fi

# run app on localhost:8080
flask --app app.py run --host localhost --port 8080

echo -e "\nVirtual environment deactivated"

# reset session
rm -r .venv
rm -r __pycache__ > /dev/null 2>&1