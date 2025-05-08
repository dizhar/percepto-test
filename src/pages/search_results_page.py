from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SearchResultsPage(BasePage):
    SORT_FIELD_DROPDOWN = (By.NAME, "sortField")

   
    def check_all_results_contain_phrase(self, phrase) -> bool:
        # Locator for all product title links
        PRODUCT_TITLES = (By.CSS_SELECTOR, "a.title_3ZxJ")
        
        # Find all product titles
        product_elements = self.find_elements(PRODUCT_TITLES)
        
        # If no results found, return False
        if not product_elements:
            return False, ["No search results found"]
        
        # Check each product title for the phrase
        missing_phrase = []
        
        for product in product_elements:
            title_text = product.text.lower()
            if phrase.lower() not in title_text:
                missing_phrase.append(title_text)

        return len(missing_phrase) == 0
        
    def click_sort_dropdown(self, timeout=10):
        dropdown = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.SORT_FIELD_DROPDOWN)
        )
        dropdown.click()    


    def select_price_asc(self, timeout=10):
        # Click the dropdown to open it
        self.click_sort_dropdown(timeout)
        # Select the price_asc option
        option = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//option[@value="price_asc"]'))
        )
        option.click()

    def check_price_sorting_ascending(self, timeout=10):
        # Locator for the price elements
        PRICE_ELEMENTS = (By.CSS_SELECTOR, ".final-price_8CiX")
        
        # Wait for the price elements to be present
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(PRICE_ELEMENTS)
        )
        
        # Find all price elements
        price_elements = self.find_elements(PRICE_ELEMENTS)
        
        # If less than 2 products, we can't determine sorting order
        if len(price_elements) < 2:
            return True
        
        # Extract prices and convert to float
        prices = []
        for element in price_elements:
            # Extract text and remove currency symbol and any whitespace
            price_text = element.text.replace('₪', '').strip()
            try:
                # Convert to float
                price = float(price_text)
                prices.append(price)
            except ValueError:
                # Skip if not a valid float
                continue
        
        # Check if the prices list is sorted in ascending order
        return prices == sorted(prices)        
    
    def handle_modal_if_displayed(self, timeout=5): 
        # Locator for the close button on the modal
        MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, ".close-btn_3jxl")
        
        for attempt in range(3):  # Try up to 3 times
            try:
                # Wait for the modal close button to be present
                close_button = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(MODAL_CLOSE_BUTTON)
                )
                
                # Click the close button to dismiss the modal
                close_button.click()
                
                # Wait briefly to ensure the modal has closed
                import time
                time.sleep(1)
                
                # Check if button is still present (modal still open)
                try:
                    self.driver.find_element(*MODAL_CLOSE_BUTTON)
                    # If we find it, continue to next attempt
                    continue
                except:
                    # Button no longer found, modal closed successfully
                    return
                    
            except TimeoutException:
                # Modal not present or not visible, which is fine
                return
    
    def select_product_by_position(self, position=3, timeout=10):
        # Convert to 0-based index for array access
        index = position - 1
        
        if index < 0:
            print(f"Invalid position: {position}. Position must be 1 or greater.")
            return False
        
        # First handle any modal that might interfere
        self.handle_modal_if_displayed()
        
        # Locator for all product links
        PRODUCT_LINKS = (By.CSS_SELECTOR, "a[data-test-id='qa-product-link']")
        
        try:
            # Wait for products to be present
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(PRODUCT_LINKS)
            )
            
            # Find all product elements
            product_elements = self.find_elements(PRODUCT_LINKS)
            
            # Check if there are enough products
            if len(product_elements) <= index:
                print(f"Only {len(product_elements)} products found, cannot select product at position {position}")
                return False
            
            # Get the product at the specified position
            target_product = product_elements[index]
            
            # Scroll to the element to ensure it's in view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_product)
            
            # Wait a moment for the scroll to complete
            import time
            time.sleep(0.5)
            
            # Click the product
            target_product.click()
            
            return True
            
        except TimeoutException:
            print("Timed out waiting for products to appear")
            return False
        except Exception as e:
            print(f"Error selecting product at position {position}: {e}")
            return False