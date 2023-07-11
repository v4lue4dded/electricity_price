import time
import os
import regex as re
import datetime as dt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# import scraping_functions as sf

# Set the directory for the files to be downloaded
download_dir = os.path.join("/home",'data')

# If the directory does not exist, create it
os.makedirs(download_dir, exist_ok=True)

with open(download_dir +"/asadf", 'w') as file:
    pass

chrome_options = webdriver.ChromeOptions()

# Add download directory to Chrome options
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
}

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--download-dir=/home/data')
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.smard.de/home/downloadcenter/download-marktdaten"
driver.get(url)
time.sleep(5) # Wait for the page to load

# Define the selectors for the dropdowns
dropdown_selectors = [
    "#help-categories select",
    "#help-subcategories select",
    "#help-regionpicker select",
    "#help-resolutionpicker select",
    "#help-filetype select"
]


# Iterate over all dropdowns
for dropdown_selector in dropdown_selectors:
    select = Select(driver.find_element(By.CSS_SELECTOR, dropdown_selector))
    options = select.options

    # Skip the first option (placeholder)
    for index in range(1, len(options)):
        print(options[index].text)
        select.select_by_index(index)
        # time.sleep(1) # Might be needed to wait for potential AJAX calls to complete


current_url = driver.current_url
from_pattern = r"%22from%22:\d+"
from_date = "2023-12-12"
from_datetime = dt.datetime.strptime(from_date, "%Y-%m-%d")
from_epoch = str(int(from_datetime.timestamp()) * 1000)
to_pattern = r"%22to%22:\d+"
to_date = "2023-12-12"
to_datetime = dt.datetime.strptime(to_date, "%Y-%m-%d")
to_epoch = str(int(to_datetime.timestamp()) * 1000)


modified_url = re.sub(from_pattern, "%22from%22:" + from_epoch, re.sub(to_pattern, "%22to%22:" + to_epoch, current_url))
driver.get(modified_url)










# Click the download button
download_button = driver.find_element(By.ID, "help-download")
download_button.click()
time.sleep(5) # Wait for the download to finish

downloaded_file_name = max([download_dir + "/" + f for f in os.listdir(download_dir)], key=os.path.getctime)

# driver.quit()


# year_dropdown.get_attribute('outerHTML')
# driver.refresh()

# print(driver.page_source)
from PIL import Image
from io import BytesIO
png = driver.get_screenshot_as_png()
im = Image.open(BytesIO(png)) 
im
