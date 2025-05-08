from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class HomePage(BasePage):
    # Locators
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-test-id="qa-header-login-button"]')
    SEARCH_BAR = (By.CSS_SELECTOR, '[data-test-id="qa-header-search-button"]')
    SEARCH_BAR_INPUT = (By.CSS_SELECTOR, '[data-test-id="qa-search-box-input"]')
   
    def __init__(self, driver):
        super().__init__(driver)
    
    def open(self):
        """Open the home page using the base URL"""
        self.navigate_to_page()
    
    def click_login_button(self):
        """Click the login button on the home page"""
        login_button = WebDriverWait(self.driver, timeout=10).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_button.click()

    def click_search_bar(self):
        """Click the search bar on the home page"""
        search_bar = WebDriverWait(self.driver, timeout=10).until(
            EC.element_to_be_clickable(self.SEARCH_BAR)
        )
        search_bar.click()

    def enter_search_phrase(self, search_text):
        # Wait for the search input field to be visible and ready
        search_input = WebDriverWait(self.driver, timeout=10).until(
            EC.visibility_of_element_located(self.SEARCH_BAR_INPUT)
        )
        
        # Clear any existing text
        search_input.clear()
        
        # Type the search text
        search_input.send_keys(search_text)
        search_input.send_keys(Keys.ENTER)
