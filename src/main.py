from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)


url = "https://www.smard.de/home/downloadcenter/download-marktdaten"
driver.get(url)


from PIL import Image
from io import BytesIO
png = driver.get_screenshot_as_png()
im = Image.open(BytesIO(png)) 
im
