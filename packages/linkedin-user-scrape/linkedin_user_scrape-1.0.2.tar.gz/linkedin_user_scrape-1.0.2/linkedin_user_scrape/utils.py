from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re


def getWebDriver(cookie, email, password):
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("disable-blink-features=AutomationControlled")
    
    link = "https://linkedin.com/uas/login"
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get(link)
    driver.implicitly_wait(10)

    username = driver.find_element(By.ID, "username")
    username.send_keys(email)

    pword = driver.find_element(By.ID, "password")
    pword.send_keys(password)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    driver.add_cookie({'name': 'li_at','value': cookie,'domain': '.linkedin.com'})

    return driver

def getDriverData(driver, url):
    driver.get(url)	 
    start = time.time()

    initialScroll = 0
    finalScroll = 1000

    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        initialScroll = finalScroll
        finalScroll += 1000

        time.sleep(3)
        end = time.time()
        if round(end - start) > 20:
            break
    src = driver.page_source

    return src



def split_at_caps(text):
  if not text:
    return []

  split_index = 1
  while split_index < len(text):
    if text[split_index].isupper() and text[split_index-1].islower():
      return [text[:split_index], text[split_index:]]
    split_index += 1
  return [text]
