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
os.chdir(download_dir)

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
# chrome_options.add_argument('--download-dir=/home/data')
# chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.smard.de/home/downloadcenter/download-marktdaten"
driver.get(url)
time.sleep(2) # Wait for the page to load


select = Select(driver.find_element(By.CSS_SELECTOR, "#help-categories select"))
options = select.options
# Skip the first option (placeholder)
for index in range(1, len(options)):
    print(options[index].text)
    select.select_by_index(index)

    select = Select(driver.find_element(By.CSS_SELECTOR, "#help-subcategories select"))
    options = select.options
    # Skip the first option (placeholder)
    for index in range(1, len(options)):
        print(options[index].text)
        select.select_by_index(index)


        # set dates
        for year in range(2018, 2023):
            print(year)
            current_url = driver.current_url
            from_pattern = r"%22from%22:\d+"
            from_date = f"{year}-01-01"
            from_datetime = dt.datetime.strptime(from_date, "%Y-%m-%d")
            from_epoch = str(int(from_datetime.timestamp()) * 1000)
            to_pattern = r"%22to%22:\d+"
            to_date = f"{year}-12-31"
            to_datetime = dt.datetime.strptime(to_date, "%Y-%m-%d")
            to_epoch = str(int(to_datetime.timestamp()) * 1000)
            modified_url = re.sub(from_pattern, "%22from%22:" + from_epoch, re.sub(to_pattern, "%22to%22:" + to_epoch, current_url))
            driver.get(modified_url)

                
            # select resolution
            select = Select(driver.find_element(By.CSS_SELECTOR, "#help-resolutionpicker select"))
            select.select_by_visible_text("Auflösung wählen: Viertelstunde")

            #select filetype 
            select = Select(driver.find_element(By.CSS_SELECTOR, "#help-filetype select"))
            select.select_by_visible_text("CSV")

            select = Select(driver.find_element(By.CSS_SELECTOR, "#help-regionpicker select"))
            select.select_by_visible_text("Land: Deutschland")




            # Click the download button
            download_button = driver.find_element(By.ID, "help-download")
            download_button.click()
            time.sleep(5) # Wait for the download to finish
            driver.refresh()

# downloaded_file_name = max([download_dir + "/" + f for f in os.listdir(download_dir)], key=os.path.getctime)

# # driver.quit()


# year_dropdown.get_attribute('outerHTML')
# driver.refresh()

# print(driver.page_source)
from PIL import Image
from io import BytesIO
png = driver.get_screenshot_as_png()
im = Image.open(BytesIO(png)) 
im
