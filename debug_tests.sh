#!/bin/bash

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    # Activate virtual environment
    source venv/bin/activate
fi

# Create necessary directories
mkdir -p reports/screenshots reports/logs

# Set environment variable for debugging
export PYTHONPATH=$(pwd)

# Run pytest with debugging flags
echo "Running tests in debug mode..."
python -m pytest src/tests/ui/test_example.py -v --no-header --pdb

echo "Debug session completed."
