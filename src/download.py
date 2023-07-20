import time
import os
import regex as re
import datetime as dt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import glob
# import scraping_functions as sf

# Set the directory for the files to be downloaded
download_dir = os.path.join("/home",'data')
os.chdir(download_dir)

chrome_options = webdriver.ChromeOptions()

# Add download directory to Chrome options
prefs = {
    "intl.accept_languages": "en,en_US",  # Request English language
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

file_name_dict = {
    "Datenkategorie: Realisierte Erzeugung" : "Realisierte_Erzeugung" ,
    "Datenkategorie: Prognostizierte Erzeugung Day-Ahead" : "Prognostizierte_Erzeugung_Day-Ahead" ,
    "Datenkategorie: Prognostizierte Erzeugung Intraday" : "Prognostizierte_Erzeugung_Intraday" ,
    "Datenkategorie: Installierte Erzeugungsleistung" : "Installierte_Erzeugungsleistung" ,
    "Datenkategorie: Realisierter Stromverbrauch" : "Realisierter_Stromverbrauch" ,
    "Datenkategorie: Prognostizierter Stromverbrauch" : "Prognostizierter_Stromverbrauch" ,
    "Datenkategorie: Großhandelspreise" : "Gro_handelspreise" ,
    "Datenkategorie: Kommerzieller Außenhandel" : "Kommerzieller_Au_enhandel" ,
    "Datenkategorie: Physikalischer Stromfluss" : "Physikalischer_Stromfluss" ,
    "Datenkategorie: Ausgleichsenergie" : "Ausgleichsenergie" ,
    "Datenkategorie: Kosten" : "Kosten" ,
    "Datenkategorie: Primärregelreserve" : "Prim_rregelreserve" ,
    "Datenkategorie: Sekundärregelreserve" : "Sekund_rregelreserve" ,
    "Datenkategorie: Minutenreserve" : "Minutenreserve" ,
    "Datenkategorie: Exportierte Regelenergie" : "Exportierte_Regelenergie" ,
    "Datenkategorie: Importierte Regelenergie" : "Importierte_Regelenergie" ,
}


select_cat = Select(driver.find_element(By.CSS_SELECTOR, "#help-categories select"))
options_cat = select_cat.options
options_cat_len = len(options_cat)
# Skip the first option (placeholder)
for index_cat in range(1, options_cat_len):
    # duplication of finding code since it gets lost a every itteration otherwise
    select_cat = Select(driver.find_element(By.CSS_SELECTOR, "#help-categories select"))
    options_cat = select_cat.options
    print(options_cat[index_cat].text)
    select_cat.select_by_index(index_cat)

    select_sub = Select(driver.find_element(By.CSS_SELECTOR, "#help-subcategories select"))
    options_sub = select_sub.options
    options_sub_len = len(options_sub)
    # Skip the first option (placeholder)
    for index_sub in range(1, options_sub_len):
        # duplication of finding code since it gets lost a every itteration otherwise
        select_sub = Select(driver.find_element(By.CSS_SELECTOR, "#help-subcategories select"))
        options_sub = select_sub.options
        text_sub = options_sub[index_sub].text 
        print(text_sub)
        select_sub.select_by_index(index_sub)


        # set dates
        # for year in range(2018, 2019):
        for year in range(2018, 2024):
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
            # resolution = "Jahr"
            resolution = "Viertelstunde"
            select_res = Select(driver.find_element(By.CSS_SELECTOR, "#help-resolutionpicker select"))
            select_res.select_by_visible_text(f"Auflösung wählen: {resolution}")

            #select filetype 
            select_fil = Select(driver.find_element(By.CSS_SELECTOR, "#help-filetype select"))
            select_fil.select_by_visible_text("CSV")

            #select region
            select_reg = Select(driver.find_element(By.CSS_SELECTOR, "#help-regionpicker select"))
            select_reg.select_by_visible_text("Land: Deutschland")

            filename = f"{file_name_dict[text_sub]}_{from_datetime.strftime('%Y%m%d%H%M')}_{to_datetime.strftime('%Y%m%d%H%M')}_{resolution}.csv"
            print(filename)
            is_downloaded = os.path.isfile(os.path.join(download_dir, filename))
            while is_downloaded is False:
                print("downloading")
                # Click the download button
                download_button = driver.find_element(By.ID, "help-download")
                download_button.click()
                time.sleep(8) # Wait for the download to finish
                is_downloaded = os.path.isfile(os.path.join(download_dir, filename))

false_download_files = glob.glob(os.path.join(download_dir, '*Quarterhour.csv'))

# Remove (delete) each file in the list
for false_download_file in false_download_files:
    try:
        os.remove(false_download_file)
        print(f"removed: {false_download_file}")
    except Exception as e:
        print(f"Error occurred while deleting file {false_download_file}. Error message: {e}")


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
