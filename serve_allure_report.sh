#!/bin/bash

# Navigate to the allure report directory
cd reports/allure-report

# Start a simple HTTP server on port 8000
echo "Starting HTTP server for Allure report at http://localhost:8000"
echo "Press Ctrl+C to stop the server"

# Check if python3 is available, otherwise try python
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000
elif command -v python &> /dev/null; then
    python -m http.server 8000
else
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi
