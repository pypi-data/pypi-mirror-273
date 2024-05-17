import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_webdriver(cookie, email, password):
    """
    Initializes a Chrome WebDriver with optional headless mode.

    Args:
        email (str): User's email address.
        password (str): User's password.
        headless (bool, optional): Whether to run Chrome in headless mode. Defaults to True.

    Returns:
        WebDriver: An instance of the Chrome WebDriver.
    """

    options = Options()
    options.add_argument("--headless")
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://linkedin.com/uas/login")
        # Use explicit wait for login elements to avoid potential errors
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username.send_keys(email)

        pword = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        pword.send_keys(password)

        # Find login button using more generic approach in case of minor UI changes
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()
        driver.add_cookie({'name': 'li_at','value': cookie,'domain': '.linkedin.com'})


    except TimeoutException:
        print("Error: Timeout waiting for login elements.")
        driver.quit()
        return None

    return driver

def get_driver_data(driver, url, scroll_delay=3, scroll_attempts=7):
    """
    Fetches data from a URL using the provided WebDriver.

    Args:
        driver (WebDriver): An instance of the WebDriver.
        url (str): The URL to fetch data from.
        scroll_delay (int, optional): Delay (in seconds) between scroll attempts. Defaults to 3.
        scroll_attempts (int, optional): Number of attempts to scroll the page. Defaults to 7.

    Returns:
        str: The HTML source code of the fetched page.
    """

    driver.get(url)
    start = time.time()

    initial_scroll = 0
    final_scroll = 1000

    for _ in range(scroll_attempts):
        driver.execute_script(f"window.scrollTo({initial_scroll},{final_scroll})")
        initial_scroll = final_scroll
        final_scroll += 1000
        time.sleep(scroll_delay)

    end = time.time()
    if round(end - start) > scroll_delay * scroll_attempts:
        print(f"Warning: Scrolling may not have reached the full page content.")

    return driver.page_source

def split_at_caps(text):
    """
    Splits a string at uppercase characters preceded by lowercase characters.

    Args:
    text (str): The text to split.

    Returns:
    list: A list of substrings split at uppercase characters.
    """
    if not text:
      return []

    split_index = 1
    while split_index < len(text):
      if text[split_index].isupper() and text[split_index-1].islower():
        return [text[:split_index], text[split_index:]]
      split_index += 1
    return [text]
