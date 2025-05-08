from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from src.utils.config_reader import ConfigReader

class DriverFactory:
    @staticmethod
    def get_driver(browser_name=None, headless=None):
        """
        Set up and return a WebDriver instance based on the browser name
        """
        # If not specified, get from config
        if browser_name is None or headless is None:
            browser_config = ConfigReader.get_browser_config()
            browser_name = browser_name or browser_config['browser']
            headless = headless if headless is not None else browser_config['headless']
        
        # Get wait times from config
        wait_times = ConfigReader.get_wait_times()
        
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            
            # Set headless mode if configured
            if headless:
                options.add_argument("--headless")
                
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            
            # Set headless mode if configured
            if headless:
                options.add_argument("--headless")
                
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
        else:
            raise ValueError(f"Browser '{browser_name}' is not supported")
        
        driver.maximize_window()
        driver.implicitly_wait(wait_times['implicit_wait'])
        
        return driver