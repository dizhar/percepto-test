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

# Let the driver_factory.py handle Chrome driver version selection

# Check if Allure is installed
if command -v allure &> /dev/null; then
    echo "Running tests with Allure reporting..."
    pytest --alluredir=reports/allure-results ""
    
    echo "Tests completed. Serving Allure report..."
    
    # Use allure serve to directly serve the results
    # This is more reliable than generating a static report
    allure serve reports/allure-results
else
    echo "Allure not detected. Running tests with HTML reporting only..."
    pytest ""
    
    echo "Tests completed. HTML report generated at reports/report.html"
    
    # Open HTML report if available
    if [[ -f "reports/report.html" ]]; then
        if [[ "$(uname)" == "Darwin"* ]]; then
            open reports/report.html
        elif [[ "$(uname)" == "Linux"* ]]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open reports/report.html
            elif command -v sensible-browser &> /dev/null; then
                sensible-browser reports/report.html
            fi
        elif [[ "$(uname)" == "MINGW"* ]] || [[ "$(uname)" == "MSYS"* ]]; then
            start reports/report.html
        fi
    fi
fi
