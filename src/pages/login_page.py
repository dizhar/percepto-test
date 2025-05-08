from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-test-id='qa-login-email-input']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test-id='qa-login-password-input']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test-id='qa-login-submit']")
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class,'error-message') and text()='אימייל או סיסמה שגויים']")
    DASHBOARD_ELEMENT = (By.CSS_SELECTOR, "[data-test-id='qa-dashboard']")
    LOGIN_FORM = (By.XPATH, "//form[.//input[@data-test-id='qa-login-email-input']]")
    
    # Network idle state indicator
    LOADER_CONTAINER = (By.CSS_SELECTOR, ".loader-bar_Y1Jw")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def open(self):
        """Open the login page and wait for it to load completely"""
        self.logger.info("Opening login page")
        self.navigate_to_page("/login")  # Adjust path if needed
        
        # Wait for network to be idle (simulating Playwright's waitForLoadState('networkidle'))
        self.wait_for_network_idle()
        
        # Wait for login form to be visible
        try:
            self.wait_for_element_visible(self.LOGIN_FORM)
            self.logger.info("Login page opened successfully")
        except TimeoutException:
            self.logger.error("Login form not visible after page load")
            raise
    
    def wait_for_network_idle(self, timeout=10):
        """Wait for network activity to settle (no loaders visible)"""
        self.logger.debug("Waiting for network idle")
        try:
            # First check if loader is present at all
            if self.is_element_present(self.LOADER_CONTAINER, timeout=1):
                # Wait for loader to not be displayed (either removed or hidden)
                WebDriverWait(self.driver, timeout).until_not(
                    EC.presence_of_element_located(self.LOADER_CONTAINER)
                )
        except TimeoutException:
            # If loader wasn't found, that's fine - page might be loaded already
            pass
        # Additional waiting to ensure stability
        self.driver.implicitly_wait(0.5)
    
    def wait_for_login_page_ready(self):
        """Wait for login page to be fully loaded and interactive"""
        # Wait for network to settle first
        self.wait_for_network_idle()
        
    
    def enter_email(self, email):
        """Enter email in the email input field with validation"""
        self.logger.info(f"Entering email: {email}")
        self.type_text(self.EMAIL_INPUT, email)
        
        # Validate that the text was entered correctly
        entered_email = self.get_attribute(self.EMAIL_INPUT, "value")
        if entered_email != email:
            self.logger.warning(f"Email verification failed. Expected: {email}, Got: {entered_email}")
            # Retry with clear first explicitly set to True
            self.type_text(self.EMAIL_INPUT, email, clear_first=True)
    
    def enter_password(self, password):
        """Enter password in the password input field"""
        self.logger.info("Entering password")
        self.type_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click the login button and wait for response"""
        self.logger.info("Clicking login button")
         
        login_button = WebDriverWait(self.driver, timeout=10).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_button.click()
    
    def is_login_successful(self):
        self.logger.debug("Checking if login was successful")
        try:
            # Wait for dashboard element to be visible, indicating successful login
            self.wait_for_element_visible(self.DASHBOARD_ELEMENT, timeout=10)
            self.logger.info("Dashboard element found - login successful")
            return True
        except TimeoutException:
            # If dashboard element is not visible, login failed
            self.logger.info("Dashboard element not found - login failed")
            return False
    
    def get_error_message(self):
        self.logger.debug("Attempting to get error message")
        try:
            # Wait briefly for error message to appear
            error_element = self.wait_for_element_visible(self.ERROR_MESSAGE, timeout=5)
            error_text = error_element.text
            self.logger.info(f"Error message found: {error_text}")
            return error_text
        except TimeoutException:
            self.logger.info("No error message found")
            return None


    def login(self, email, password):
        """Perform login with the given credentials"""
        self.logger.info(f"Performing login with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        
        # Log the result
        if self.is_login_successful():
            self.logger.info("Login successful")
        else:
            error_msg = self.get_error_message() or "Unknown error"
            self.logger.warning(f"Login failed: {error_msg}")