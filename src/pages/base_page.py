from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.find_element(locator).click()

    def send_keys(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        
    def type_text(self, locator, text):
        """Type text into an element (alias for send_keys for compatibility)"""
        self.send_keys(locator, text)
        
    def navigate_to_page(self, path=""):
        """Navigate to a specific path on the site"""
        base_url = "https://www.terminalx.com"
        self.driver.get(f"{base_url}{path}")
        
    def is_element_displayed(self, locator, timeout=10):
        """Check if an element is displayed"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
            
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for an element to be visible"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        
    def wait_for_element_clickable(self, locator, timeout=10):
        """Wait for an element to be clickable"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        
    def get_text(self, locator):
        """Get text from an element"""
        return self.find_element(locator).text
        
    def get_attribute(self, locator, attribute):
        """Get attribute value from an element"""
        return self.find_element(locator).get_attribute(attribute)
        
    def get_css_property(self, locator, property_name):
        """Get CSS property value from an element"""
        return self.find_element(locator).value_of_css_property(property_name)
