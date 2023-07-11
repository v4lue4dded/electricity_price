from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains


from datetime import datetime

def select_date(driver, date, daterange_name):
    # Verify the date
    try:
        datetime_object = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("This is not a valid date")
    
    year = datetime_object.year
    month = datetime_object.month - 1  # subtract 1 as per your requirement
    day = datetime_object.day
    
    # Remove leading zeros
    str_year = str(year)
    str_month = str(month).lstrip("0") if month > 0 else "0"
    str_day = str(day).lstrip("0")
    
    print(f"Year: {year}, Month: {month}, Day: {day}")
    
    # Set the date range manually - this needs to be adapted if the website requires a different method for date selection
    daterange = driver.find_element(By.NAME, daterange_name)
    daterange.click()
    datepicker = driver.find_element(By.CLASS_NAME, 'daterangepicker')
    month_dropdown = datepicker.find_element(By.CLASS_NAME, 'monthselect')
    Select(month_dropdown).select_by_value(str_month)
    
    # Select the desired month and year
    
    year_dropdown = datepicker.find_element(By.CLASS_NAME, 'yearselect')    
    Select(year_dropdown).select_by_value(str_year)
    
    calendar_table = datepicker.find_element(By.CLASS_NAME, 'calendar-table')
    # Now we select the day. This assumes the days are the td elements in your table.
    # If they're different elements, you'll need to adjust the code.
    
    # For this example, we'll select the specified day of the month
    day_elements = calendar_table.find_elements(By.TAG_NAME, 'td')
    
    for day_element in day_elements:
        print(day_element)
        print(day_element.get_attribute('outerHTML'))
        if "off" not in day_element.get_attribute('class'):
            print("blub")
            print(day_element.get_attribute('innerHTML') )
            print("blub")
            if day_element.get_attribute('innerHTML') == str_day:
                print("wqfeqwefawef")
                actions = ActionChains(driver)
                actions.move_to_element(day_element)
                # Perform the click action
                actions.click().perform()
                
                day_element.click()


                break


from PIL import Image
from io import BytesIO
png = driver.get_screenshot_as_png()
im = Image.open(BytesIO(png)) 
im
