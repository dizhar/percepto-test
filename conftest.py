import pytest
import allure
import os
from datetime import datetime
from src.utils.driver_factory import DriverFactory
from src.utils.config_reader import ConfigReader

def pytest_configure(config):
    """Set up the Allure environment"""
    if not os.path.exists('reports/allure-results'):
        os.makedirs('reports/allure-results')
    
    # Create environment.properties file for Allure
    allure_env_path = 'reports/allure-results/environment.properties'
    with open(allure_env_path, 'w') as f:
        f.write(f"Browser=Chrome\n")
        f.write(f"Browser.Version=latest\n")
        f.write(f"Environment=Test\n")
        f.write(f"Test.Framework=Pytest\n")
        f.write(f"Python.Version={pytest.__version__}\n")
        f.write(f"Timestamp={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

@pytest.fixture(scope="function")
def driver(request):
    """
    Set up and tear down the WebDriver
    """
    # Read the configuration
    try:
        config = ConfigReader.read_config()
        browser = config.get('Browsers', 'browser')
    except:
        browser = "chrome"
    
    # Set up the driver
    driver = DriverFactory.get_driver(browser)
    
    # Add allure environment info - using attach instead of environment
    allure.attach(
        f"Browser: {browser}",
        name="environment-info",
        attachment_type=allure.attachment_type.TEXT
    )
    
    # Pytest fixture metadata for Allure
    test_name = request.node.name
    allure.dynamic.title(test_name)
    
    # Return the driver to the test
    yield driver
    
    # Take screenshot on test failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"failure_{test_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except:
            pass
    
    # Tear down the driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test outcomes for the driver fixture
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
