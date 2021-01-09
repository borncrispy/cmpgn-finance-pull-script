import re
import time
from datetime import datetime as dt
from random import randint

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


def create_driver(path: str):
    """
    Creates a Firefox gecko driver to download find and download resources since there is no API or simple
    way to access data. Driver is created with a profile that allows us to skip download dialog box and
    save files to specific location.
    var path: string: user specified path for downloads
    return: Gecko driver
    """
    # set up browser profile to avoid download box dialog
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList',
                           2)  # 0 is desktop, 1 is the download folder, and 2 indicates a custom (see: browser.download.dir) folder
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir',
                           '/Users/lsward/develop/github.borncrispy/cmpgn-finance-pull-script/data')
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

    # create webdriver and go to search page
    return webdriver.Firefox(profile)


def pull_finance_data():
    """
    Pulls financial contribution data by locating date fields, filling them out, locating search button, clicking on
    search button, waiting for download button to load, and clicking on download button.
    """
    driver = create_driver()
    driver.get('https://cf.ncsbe.gov/CFTxnLkup/')

    # wait for search page to load
    try:
        WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.ID, 'btnSearch')))
        print('Search page is loaded')
    except TimeoutException:
        print('Load took too much time.')

    # adding wait for now to slow down progress
    time.sleep(randint(41, 70))
    driver.implicitly_wait(randint(137, 371))

    # create search dates
    delta = dt.today() - relativedelta(months=1)
    to_date = dt.today().strftime('%m/%d/%Y')
    from_date = delta.strftime('%m/%d/%Y')

    # enter in dates and click on search button
    from_date_field = driver.find_element_by_id('DateFrom')  # first field with earlier date
    from_date_field.send_keys(from_date)
    driver.implicitly_wait(randint(121, 301))
    time.sleep(randint(10, 15))
    to_date_field = driver.find_element_by_id('DateTo')  # second field with today's date or later date
    to_date_field.send_keys(to_date)
    search_button = driver.find_element_by_id('btnSearch')
    time.sleep(randint(12, 23))
    driver.implicitly_wait(randint(121, 301))
    search_button.click()

    print('Searching...')

    # wait for results to load (this take a long time - need to keep an eye on wait time)
    try:
        WebDriverWait(driver, 160).until(ec.presence_of_element_located((By.ID, 'btnExportResults')))
        print('Data is ready to export')
    except TimeoutException:
        print('Load took too much time.')

    # adding wait for now to slow down progress
    time.sleep(randint(45, 60))
    driver.implicitly_wait(randint(137, 371))

    # once page loads, click on export results button
    export_button = driver.find_element_by_id('btnExportResults')
    time.sleep(randint(37, 63))
    driver.implicitly_wait(randint(137, 371))
    export_button.click()

    print('Exporting results....')

    # wait for download to complete and close browser session
    driver.implicitly_wait(randint(137, 371))
    # driver.close()


def pull_committee_data(type: str):
    """
    Pull campaign committee data by locating check boxes, determining if it is a report or doc, checking box, finding
    search button, waiting for download link to become available, and clicking on download link.
    var type: string: the type of document that is being searched for
    """
    driver = create_driver()
    driver.get('https://cf.ncsbe.gov/CFDocLkup/')

    time.sleep(randint(4, 7))

    # document download, need a report download too
    for x in range(1, 10):  # 1-45 document, 46-81 report
        checkbox = driver.find_element_by_xpath(f"/html/body/div[2]/div[2]/div/form/div/div/div/div[2]/div[2]/div/table/tbody/tr[{x}]/td[1]")
        checkbox.click()

    search_button = driver.find_element_by_id('btnSearch')
    search_button.click()

    print('Searching...')
    try:
        WebDriverWait(driver, 160).until(ec.presence_of_element_located((By.LINK_TEXT, 'Export list to .CSV')))
        print('Data is ready to export')
    except TimeoutException:
        print('Load took too much time.')

    time.sleep(randint(10, 20))
    # Looking for the number of results to determine the number resources I need to gather
    test = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div/div/div[1]").text
    number = re.findall(r'\d+', test)
    print(f'There are {number} links that need to be harvested')

    # Export committee csv
    export_link = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div/div/div[1]/center/a")
    export_link.click()


pull_committee_data()
