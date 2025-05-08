@echo off
:: Create and activate virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    
    :: Activate virtual environment
    call venv\Scripts\activate
    
    :: Install dependencies
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    :: Activate virtual environment
    call venv\Scripts\activate
)

:: Create necessary directories
if not exist reports mkdir reports
if not exist reports\screenshots mkdir reports\screenshots
if not exist reports\logs mkdir reports\logs

:: Let the driver_factory.py handle Chrome driver version selection

:: Check if Allure is installed
where allure >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Running tests with Allure reporting...
    pytest --alluredir=reports\allure-results %*
    
    echo Tests completed. Serving Allure report...
    
    :: Use allure serve to directly serve the results
    :: This is more reliable than generating a static report
    allure serve reports\allure-results
) else (
    echo Allure not detected. Running tests with HTML reporting only...
    pytest %*
    
    echo Tests completed. HTML report generated at reports\report.html
)
