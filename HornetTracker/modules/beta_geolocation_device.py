from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeType

def getLocation():
    options = Options()
    # options.add_argument("headless")
    options.add_argument('window-size=800x600')
    options.add_argument("disable-gpu")
    options.add_argument("--use--fake-ui-for-media-stream")
    driver = webdriver.Chrome(ChromeDriverManager(
        chrome_type=ChromeType.CHROMIUM).install(), chrome_options=options)
    timeout = 20
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    latitude = driver.find_element(By.ID, 'latitude').text  # Replace with ID name -
    longitude = driver.find_element(By.ID, 'longitude').text
    # latitude = [x.text for x in latitude]
    # latitude = str(latitude[0])
    driver.quit()

    return {"latitude":f"{latitude}","longitude":f"{longitude}"}


print(getLocation())
