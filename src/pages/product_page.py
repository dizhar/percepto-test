from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.pages.base_page import BasePage

class ProductPage(BasePage):
    PRICE_ELEMENT = (By.CSS_SELECTOR, "[data-test-id='qa-pdp-price-final']")

    def has_price(self, timeout=10):
        try:
            # Wait for the price element to be present
            price_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.PRICE_ELEMENT)
            )
            
            # Check if the price text is not empty
            price_text = price_element.text.strip()
            return bool(price_text)
            
        except TimeoutException:
            print("Price element not found within timeout period")
            return False
        except Exception as e:
            print(f"Error checking for price: {e}")
            return False
    
    def get_css_rule_font_size(self, class_name="prices-final_1R9x"):
        # JavaScript to find the CSS rule and get its font-size property
        script = """
            function getStyleRuleValue(style, selector, property) {
                try {
                    for (var i = 0; i < document.styleSheets.length; i++) {
                        var sheet = document.styleSheets[i];
                        if (!sheet.cssRules) { continue; } // Skip if no rules (e.g., cross-origin)
                        
                        for (var j = 0; j < sheet.cssRules.length; j++) {
                            var rule = sheet.cssRules[j];
                            if (rule.selectorText && rule.selectorText.includes(selector)) {
                                return rule.style.getPropertyValue(property);
                            }
                        }
                    }
                } catch (e) {
                    console.error("Error accessing styleSheets:", e);
                }
                return null;
            }
            
            return getStyleRuleValue(document.styleSheets, arguments[0], 'font-size');
        """
        
        try:
            # Execute the script to get the font-size from the CSS rule
            font_size = self.driver.execute_script(script, class_name)
            
            if font_size:
                # Clean up the result (remove extra spaces, etc.)
                font_size = font_size.strip()
                print(f"Found font-size in CSS rule for {class_name}: {font_size}")
                return font_size
            else:
                print(f"Could not find font-size in CSS rule for {class_name}")
                return None
                
        except Exception as e:
            print(f"Error getting CSS rule font-size: {e}")
            return None

    def is_price_font_size_correct(self, expected_size="1.8rem"):
        # Get the font-size from the CSS rule
        font_size = self.get_css_rule_font_size("prices-final_1R9x")
        
        if font_size is None:
            return False
        
        # Compare with expected value
        return font_size == expected_size