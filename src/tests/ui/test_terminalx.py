import json
import random
import allure
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.pages.product_page import ProductPage
from src.pages.search_results_page import SearchResultsPage
import pytest_check as check 

@allure.epic("TerminalX E-commerce")
@allure.feature("Shopping Workflow")
@allure.story("End-to-End Shopping Experience")
@allure.description("""
This test verifies the end-to-end shopping workflow on TerminalX website:
1. Login with random user credentials
2. Search for products using the search bar
3. Verify search results contain expected phrase
4. Sort products by price (ascending)
5. Verify correct price sorting
6. Select a specific product
7. Verify product price display and font-size
""")
def test_terminalx_workflow(driver):
    with allure.step("Load user credentials from JSON file"):
        with open("src/data/users.json") as f:
            users = json.load(f)["users"]
        user = random.choice(users)
        allure.attach(f"Username: {user['username']}", name="Selected User", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Initialize page objects"):
        home_page = HomePage(driver)
        login_page = LoginPage(driver)
        search_results_page = SearchResultsPage(driver)
        product_page = ProductPage(driver)

    with allure.step("Open TerminalX website"):
        home_page.navigate_to_page()
        allure.attach(driver.get_screenshot_as_png(), name="Homepage Loaded", attachment_type=allure.attachment_type.PNG)

    with allure.step(f"Login with user: {user['username']}"):
        home_page.click_login_button()
        allure.attach(driver.get_screenshot_as_png(), name="Login Form", attachment_type=allure.attachment_type.PNG)
        login_page.login(user['username'], user['password'])
        allure.attach(driver.get_screenshot_as_png(), name="After Login", attachment_type=allure.attachment_type.PNG)

    with allure.step("Search for 'hello' in the search bar"):
        home_page.click_search_bar()
        allure.attach(driver.get_screenshot_as_png(), name="Search Bar Clicked", attachment_type=allure.attachment_type.PNG)
        home_page.enter_search_phrase("hello")
        allure.attach(driver.get_screenshot_as_png(), name="Search Phrase Entered", attachment_type=allure.attachment_type.PNG)

    with allure.step("Verify search results contain 'hello kitty'"):
        have_all_the_results_contain_phrase = search_results_page.check_all_results_contain_phrase("hello kitty")
        check.is_true(have_all_the_results_contain_phrase, "Not all search results contain the phrase 'hello kitty'")
        allure.attach(str(have_all_the_results_contain_phrase), name="Search Results Validation", attachment_type=allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), name="Search Results", attachment_type=allure.attachment_type.PNG)

    with allure.step("Sort products by price (ascending)"):
        search_results_page.handle_modal_if_displayed()
        allure.attach(driver.get_screenshot_as_png(), name="Before Sorting", attachment_type=allure.attachment_type.PNG)
        search_results_page.select_price_asc()
        allure.attach(driver.get_screenshot_as_png(), name="After Sorting", attachment_type=allure.attachment_type.PNG)

    with allure.step("Verify products are sorted by price ascending"):
        is_prices_sorted_from_cheapest_to_most_expensive = search_results_page.check_price_sorting_ascending()
        check.is_true(is_prices_sorted_from_cheapest_to_most_expensive, "Not all the prices are sorted from cheapest to most expensive")
        allure.attach(str(is_prices_sorted_from_cheapest_to_most_expensive), name="Price Sorting Validation", attachment_type=allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), name="Sorted Products", attachment_type=allure.attachment_type.PNG)

    with allure.step("Navigate to the third product in search results"):
        allure.attach(driver.get_screenshot_as_png(), name="Before Product Selection", attachment_type=allure.attachment_type.PNG)
        search_results_page.select_product_by_position(3)
        allure.attach(driver.get_screenshot_as_png(), name="After Product Selection", attachment_type=allure.attachment_type.PNG)

    with allure.step("Verify product price display and font size"):
        price_displayed = product_page.has_price()
        is_font_size_correct = product_page.is_price_font_size_correct()
        check.is_true(price_displayed, "Product price is not displayed")
        check.is_true(is_font_size_correct, "Product price size in not 1.8rem")
        allure.attach(str(price_displayed), name="Price Display Validation", attachment_type=allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(), name="Product Price Display", attachment_type=allure.attachment_type.PNG)