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

# Check if Allure is installed
if command -v allure &> /dev/null; then
    echo "Running tests with Allure reporting..."
    pytest --alluredir=reports/allure-results ""
    
    # Generate Allure report
    allure generate reports/allure-results -o reports/allure-report --clean
    
    echo "Tests completed. Allure report generated at reports/allure-report/index.html"
    
    # Serve and open the Allure report using allure open command
    echo "Starting Allure server and opening report..."
    
    # Run allure open in the background
    allure open reports/allure-report &
    
    # Store the process ID of the allure server
    ALLURE_PID=$!
    
    # Wait for user to press any key to continue
    echo "Allure report server started. Press any key to stop the server and continue..."
    read -n 1 -s
    
    # Kill the allure server process when user presses key
    kill $ALLURE_PID 2>/dev/null || true
else
    echo "Allure not detected. Running tests with HTML reporting only..."
    pytest ""
    
    echo "Tests completed. HTML report generated at reports/report.html"
    
    # Start a simple HTTP server for HTML report
    echo "Starting HTTP server for HTML report..."
    (cd reports && python3 -m http.server 8000 &)
    SERVER_PID=$!
    
    # Open the report in browser
    if [[ "$(uname)" == "Darwin"* ]]; then
        open http://localhost:8000/report.html
    elif [[ "$(uname)" == "Linux"* ]]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:8000/report.html
        elif command -v sensible-browser &> /dev/null; then
            sensible-browser http://localhost:8000/report.html
        fi
    elif [[ "$(uname)" == "MINGW"* ]] || [[ "$(uname)" == "MSYS"* ]]; then
        start http://localhost:8000/report.html
    fi
    
    # Wait for user to press any key to continue
    echo "HTML report server started. Press any key to stop the server and continue..."
    read -n 1 -s
    
    # Kill the server process when user presses key
    kill $SERVER_PID 2>/dev/null || true
fi