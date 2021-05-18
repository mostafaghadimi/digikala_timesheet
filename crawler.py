import os
import time
import codecs
import logging
import subprocess

import pandas as pd
from selenium import webdriver
from dotenv import dotenv_values
from selenium.webdriver.common.keys import Keys

from enums import RowDetails, ExcelColNames, WebElements


def submit_timesheet(driver, base_dir):
    try:
        driver.get('http://172.16.190.132/HcmDigikala/defaultportal/Core/Index%5D?board=LeaveRequestBoard')
        df = pd.read_excel(os.path.join(base_dir, 'timesheet/timesheet.xlsx'))
                
        for _, row in df.iterrows():
            date = row[ExcelColNames.DATE.value]
            type = row[ExcelColNames.TYPE.value]
            status = row[ExcelColNames.STATUS.value]
            to_hour = row[ExcelColNames.TO_HOUR.value]
            from_hour = row[ExcelColNames.FROM_HOUR.value]

            while driver.find_element_by_id(WebElements.STATUS.value).get_attribute("value") != status:
                driver.find_element_by_id(WebElements.STATUS.value).send_keys(Keys.ARROW_DOWN)

            if type == RowDetails.HOURLY.value:
                flag = True
                while driver.find_element_by_id(WebElements.TYPE.value).get_attribute("value") != RowDetails.HOURLY.value:
                    if flag:
                        driver.find_element_by_id(WebElements.TYPE.value).send_keys(Keys.CONTROL, 'a', Keys.NULL, Keys.BACKSPACE)
                        driver.find_element_by_id(WebElements.TYPE.value).send_keys('س')
                    flag = False
                    driver.find_element_by_id(WebElements.TYPE.value).send_keys(Keys.ARROW_DOWN)
                    if driver.find_element_by_id(WebElements.TYPE.value).get_attribute("value") == RowDetails.HOURLY.value:
                        driver.find_element_by_id(WebElements.TYPE.value).send_keys(Keys.TAB)

                time.sleep(0.3)
                driver.find_element_by_id(WebElements.HOURLY_START_DATE.value).send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, date)
                driver.find_element_by_id(WebElements.HOURLY_END_DATE.value).send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, date)
                driver.find_element_by_id(WebElements.HOURLY_FROM_HOUR.value).send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, from_hour)
                driver.find_element_by_id(WebElements.HOURLY_TO_HOUR.value).send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, to_hour)
            else:
                driver.find_element_by_id(WebElements.DAILY_START_DATE.value).send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, date)
                driver.find_element_by_id(WebElements.DAILY_END_DATE.value).send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, date)

            driver.find_element_by_id(WebElements.SAVE_BUTTON.value).click()

    except Exception as e:
        print(e)
        # logging.error("logging was unsuccessful")

def login(driver, base_dir):
    # Reading username and password from credentials.env file
    config = dotenv_values(os.path.join(base_dir, "credentials.env"))
    username = config['HRMS_USERNAME']
    password = config['HRMS_PASSWORD']

    driver.find_element_by_id("UserName").send_keys(username)
    driver.find_element_by_id("Password").send_keys(password)
    driver.find_element_by_id("Login").click()


def get_driver_path(base_dir):
    return os.path.join(base_dir, 'driver/chromedriver')


def download_chrome_driver():
    """
    This method will download the required google chrome driver.
    """
    # TODO://
    pass


def check_chrome_driver_unix(base_dir):
    """
    This method checks whether the installed Google-Chrome driver existed on the ./drivers/ path and is compatible with the current version of Google-Chrome or not. 
    The first argument indicates whether google-chrome is installed or not
    The second argument indicates whether driver is existing or not
    """
    try:
        gc = subprocess.check_output("google-chrome --version", shell=True)
        gc = codecs.decode(gc) # convert bytes to str
        gc_version = gc.split()[2]
        if os.path.isfile(os.path.join(base_dir, 'driver/chromedriver')):
            return True, True
        logging.error("You should download {} chromedriver from the following link: \nhttps://chromedriver.storage.googleapis.com/index.html".format(gc_version))    
        return True, False

    except Exception as e:
        print(e)
        logging.error("Make sure you have installed Chrome properly")
        return False, False
    


if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    chrome_flag, driver_flag = check_chrome_driver_unix(base_dir)
    driver = webdriver.Chrome(executable_path=get_driver_path(base_dir))
    try:
        driver.get('http://172.16.190.132/HcmDigikala/Account/Login?ReturnUrl=%2fhcmdigikala')
    except:
        logging.error("Make sure your company VPN is on or you might turn the other VPNs off.")
    login(driver, base_dir)
    submit_timesheet(driver, base_dir)