# import os
# import requests
from dateutil.relativedelta import relativedelta
from random import randint
from datetime import datetime as dt

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

# set up browser profile to avoid download box dialog
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)  # 0 is desktop, 1 is the download folder, and 2 indicates a custom (see: browser.download.dir) folder
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('broswer.download.dir', '/Users/lsward/develop/gitlab/personal/cmpgn-finance-dash')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

# create webdriver and go to search page
driver = webdriver.Firefox(profile)
driver.get('https://cf.ncsbe.gov/CFTxnLkup/AdvancedSearch/')

# wait for search page to load
try:
    WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.ID, 'btnSearch')))
    print('Search page is loaded')
except TimeoutException:
    print('Load took too much time.')

driver.implicitly_wait(randint(137, 371))

# create search dates
delta = dt.today() - relativedelta(months=3)
to_date = dt.today().strftime('%m/%d/%Y')
from_date = delta.strftime('%m/%d/%Y')

# enter in dates and click on search button
from_date_field = driver.find_element_by_id('DateFrom')  # first field with earlier date
from_date_field.send_keys(from_date)
driver.implicitly_wait(randint(121, 301))
to_date_field = driver.find_element_by_id('DateTo')  # second field with today's date or later date
to_date_field.send_keys(to_date)
search_button = driver.find_element_by_id('btnSearch')
driver.implicitly_wait(randint(121, 301))
search_button.click()

print('Searching...')

# wait for results to load (this take a long time - need to keep an eye on wait time)
try:
    WebDriverWait(driver, 160).until(ec.presence_of_element_located((By.ID, 'btnExportResults')))
    print('Data is ready to export')
except TimeoutException:
    print('Load took too much time.')

driver.implicitly_wait(randint(137, 371))

# once page loads, click on export results button
export_button = driver.find_element_by_id('btnExportResults')
driver.implicitly_wait(randint(137, 371))
export_button.click()

print('Exporting results....')

# wait for download to complete and close browser session
driver.implicitly_wait(randint(137, 371))
# driver.close()





