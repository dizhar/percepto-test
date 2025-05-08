# Percepto-Test Framework

A Python-based testing framework using Selenium and pytest for UI testing of the TerminalX website. This framework implements the Page Object Model design pattern for maintainable and scalable test automation. It includes comprehensive Allure reporting.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome or Firefox browser

### Installation

1. Clone the repository:

   ```
   git clone git@github.com:dizhar/percepto-test.git
   cd percepto-test
   ```

2. Create and activate a virtual environment:

   ```
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Download browser drivers:

   ```
   # On macOS/Linux
   chmod +x download_drivers.sh
   ./download_drivers.sh

   # On Windows
   # Use the webdriver-manager which is included in the requirements
   # The framework will automatically download the drivers when needed
   ```

5. Install Allure (for reports):

   ```
   # On Windows (using Scoop)
   scoop install allure

   # On macOS
   brew install allure

   # On Linux
   sudo apt-add-repository ppa:qameta/allure
   sudo apt-get update
   sudo apt-get install allure
   ```

## Running Tests

### Basic Test Execution

```
# Run all tests
pytest

# Run specific test file
pytest src/tests/ui/test_terminalx.py

# Run with verbose output
pytest -v
```

### Using the Provided Scripts

```
# Run tests and generate reports (macOS/Linux)
chmod +x run_tests.sh
./run_tests.sh

# Run tests and generate reports (Windows)
run_tests.bat


# Serve Allure report via HTTP server (if you have issues viewing the report)
chmod +x serve_allure_report.sh
./serve_allure_report.sh
```

### Generating Reports

#### HTML Report

The HTML report is automatically generated in the reports directory when you run the tests.

#### Allure Report

The framework uses Allure for comprehensive test reporting.

```
# Run tests with Allure results collection
pytest --alluredir=reports/allure-results

# Generate and view Allure report (recommended method)
allure serve reports/allure-results
```

**Note:** When opening Allure reports directly from the file system (using `file://` protocol),
browsers may block the report from loading due to CORS security restrictions.
To avoid this issue, always serve the report using a web server like `allure serve`
or the provided `serve_allure_report.sh` script.

## Project Structure

```
percepto-test/
│
├── src/                         # source code directory
│   ├── pages/                   # page object models for UI tests
│   │   ├── base_page.py         # base page with common methods
│   │   ├── home_page.py         # TerminalX home page
│   │   ├── login_page.py        # TerminalX login page
│   │   ├── product_page.py      # TerminalX product page
│   │   └── search_results_page.py # TerminalX search results page
│   ├── utils/                   # utility functions and helpers
│   │   ├── driver_factory.py    # WebDriver initialization
│   │   ├── config_reader.py     # Configuration reader
│   │   ├── api_utils.py         # API utilities
│   │   └── test_data.py         # Test data utilities
│   ├── config/                  # configuration files
│   │   └── config.ini           # Main configuration
│   ├── data/                    # test data
│   │   └── users.json           # User credentials
│   └── tests/                   # test directory
│       └── ui/                  # UI tests with Selenium
│           └── test_terminalx.py # TerminalX UI tests
│
├── conftest.py                  # pytest fixtures and configuration
├── pytest.ini                   # pytest configuration
├── requirements.txt             # project dependencies
├── run_tests.sh                 # script to run tests (Unix)
├── run_tests.bat                # script to run tests (Windows)
├── serve_allure_report.sh       # script to serve Allure report
├── download_drivers.sh          # script to download browser drivers
│
└── reports/                     # test reports and logs
    ├── screenshots/             # failure screenshots (generated during test runs)
    ├── logs/                    # test execution logs (generated during test runs)
    ├── allure-results/          # Allure raw results (generated during test runs)
    └── allure-report/           # Generated Allure report (generated during test runs)
```

## Configuration

Update the configuration file in the `src/config` directory to change:

- Test environments (`config.ini`)
- Browser settings (`config.ini`)
- Timeouts and other settings (`config.ini`)

### config.ini

The main configuration file contains settings for:

- Base URL (currently set to TerminalX URL)
- Browser settings (browser type, headless mode, etc.)
- Wait timeouts
- Screenshot settings

## Adding New Tests

1. Create a new test file in `src/tests/ui/`
2. Follow the existing patterns in `test_terminalx.py` and use the provided base classes
3. Use the Page Object Model pattern for maintainability

## Debugging Tests

You can use the Python debugger (pdb) or the VSCode debugger to debug your tests:

```python
# Add this line where you want to set a breakpoint
import pdb; pdb.set_trace()
```

Alternatively, you can use the VSCode debugging configuration in `.vscode/launch.json` to run and debug tests directly from the editor.

## CI/CD Integration

This framework can be integrated with CI/CD pipelines such as Jenkins, GitHub Actions, or GitLab CI. The key steps for integration are:

1. Install dependencies: `pip install -r requirements.txt`
2. Download browser drivers: `./download_drivers.sh`
3. Run tests: `pytest` or `./run_tests.sh`
4. Generate and publish reports: `allure generate reports/allure-results -o reports/allure-report --clean`
