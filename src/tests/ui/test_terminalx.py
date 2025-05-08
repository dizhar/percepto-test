import json
import random
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.pages.product_page import ProductPage
from src.pages.search_results_page import SearchResultsPage
import pytest_check as check 

def test_terminalx_workflow(driver):
     # Load user credentials
    with open("src/data/users.json") as f:
        users = json.load(f)["users"]
    user = random.choice(users)
    
   # Initialize pages
    home_page = HomePage(driver)
    login_page = LoginPage(driver)
    search_results_page = SearchResultsPage(driver)
    product_page = ProductPage(driver)

    # 1. Open TerminalX website
    home_page.navigate_to_page()

    # 2. Login with random user
    home_page.click_login_button()
    login_page.login(user['username'], user['password'])

    # 3. Enter "hello" in search bar
    home_page.click_search_bar()
    home_page.enter_search_phrase("hello")

    # 4. Check dropdown results contain "hello kitty" - USING SOFT ASSERTIONS
    have_all_the_results_contain_phrase = search_results_page.check_all_results_contain_phrase("hello kitty")
    check.is_true(have_all_the_results_contain_phrase, "Not all search results contain the phrase 'hello kitty'")

    # 5. Check if products are sorted by price ascending
    search_results_page.handle_modal_if_displayed()
    search_results_page.select_price_asc()

    is_prices_sorted_from_cheapest_to_most_expensive = search_results_page.check_price_sorting_ascending()
    check.is_true(is_prices_sorted_from_cheapest_to_most_expensive, "Not all the prices are sorted from cheapest to most expensive")

    # 6. Go to the third result
    search_results_page.select_product_by_position(3)

    # 7. Check price exists and font size is 1.8rem
    check.is_true(product_page.has_price(), "product price is not displayed")
    check.is_true(product_page.is_price_font_size_correct(), "the price font size is not 1.8rem")
