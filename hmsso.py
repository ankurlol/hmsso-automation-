"""
Automation starter for hmsso.coalindia.in
Requires: pip install selenium webdriver-manager
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://hmsso.coalindia.in"


def get_driver(headless: bool = False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def open_site(driver):
    driver.get(URL)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("Page loaded:", driver.title)


def login(driver, username, password):
    # NOTE: selector names below are best-guess placeholders.
    # Open the real login page, right-click the username field -> Inspect,
    # and update By.ID / By.NAME values to match the actual HTML.
    user_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "txtUserName"))
    )
    user_field.clear()
    user_field.send_keys(username)

    pass_field = driver.find_element(By.ID, "txtPassword")
    pass_field.clear()
    pass_field.send_keys(password)

    login_btn = driver.find_element(By.ID, "btnLogin")
    login_btn.click()

    WebDriverWait(driver, 15).until(
        EC.staleness_of(login_btn)
    )
    print("Logged in.")


def click_menu_item(driver, link_text, wait_time=10):
    """Click a menu/link by its visible text (expands submenus, etc)."""
    elem = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text))
    )
    elem.click()
    print(f"Clicked: {link_text}")


def navigate_to_opd_register(driver):
    # MIS Report -> expand
    click_menu_item(driver, "MIS Report")
    # Report -> expand
    click_menu_item(driver, "Report")
    # OPD Register -> click
    click_menu_item(driver, "OPD Register")


def main():
    driver = get_driver(headless=False)
    try:
        open_site(driver)
        login(driver, "GNHADMIN", "gandhinagar@2025")
        navigate_to_opd_register(driver)
        input("Press Enter to close browser...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()