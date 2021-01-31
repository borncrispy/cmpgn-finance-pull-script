import re
import os
import sys
import csv
import time
from datetime import datetime as dt
from random import randint

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select

from bs4 import BeautifulSoup as bs

current_dir = os.path.dirname(os.path.abspath(__file__))


def leap_year_bulk():
    """
    This function is used to help in puling historical data.
    """


def rename_file(from_date, to_date):
    path = '/Users/lsward/develop/github.borncrispy/cmpgn-finance-pull-script/data'
    original_file = '/transinq_results.csv'
    new_file = f'/{from_date.replace("/", "")}-{to_date.replace("/", "")}.csv'
    if os.path.exists(f'{path}{original_file}'):
        os.rename(f'{path}{original_file}', f'{path}{new_file}')
    else:
        print(f'File does not exist for timeframe ({from_date}-{to_date})')


def historic_finance_pull(year):
    months = ['12', '11', '10', '09', '08', '07', '06', '05', '04', '03', '02', '01']
    leap_years = [2020, 2016, 2012, 2008, 2004, 2000, 1996, 1992, 1988, 1984, 1980]
    from_date = ''
    to_date = ''
    for month in months:
        if month == '01':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/31/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '03':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/31/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '04':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/30/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '05':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/31/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '06':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/30/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '07':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/31/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '08':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/31/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '09':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/30/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '10':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/31/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '11':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/30/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '12':
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/31/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        elif month == '02' and int(year) in leap_years:
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/29/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)
        else:
            from_date = f'{month}/01/{year}'
            to_date = f'{month}/28/{year}'
            wd, has_file = pull_finance_data(from_date, to_date)

        if has_file:
            time.sleep(randint(3, 37))
            wd.close()
            rename_file(from_date, to_date)
        else:
            wd.close()

        print('\n')


def create_driver():
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


def pull_finance_data(from_date='', to_date=''):
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

    # create search dates
    if not from_date and not to_date:
        # set search dates
        delta = dt.today() - relativedelta(months=1)
        to_date = dt.today().strftime('%m/%d/%Y')
        from_date = delta.strftime('%m/%d/%Y')

    # enter in dates and click on search button
    from_date_field = driver.find_element_by_id('DateFrom')  # first field with earlier date
    from_date_field.send_keys(from_date)
    to_date_field = driver.find_element_by_id('DateTo')  # second field with today's date or later date
    to_date_field.send_keys(to_date)
    search_button = driver.find_element_by_id('btnSearch')
    print(f'Searching timeframe({from_date}-{to_date})...')
    search_button.click()

    # wait for results to load (this take a long time - need to keep an eye on wait time)
    try:
        WebDriverWait(driver, 160).until(ec.presence_of_element_located((By.ID, 'btnExportResults')))
        if driver.find_element_by_id('divNoRecords').text:
            with open(f'{current_dir}/data/{from_date.replace("/", "")}-{to_date.replace("/", "")}.csv',
                      'w') as no_rec_file:
                no_rec_file.write(driver.find_element_by_id('divNoRecords').text)
            print(f'No records found for timerange({from_date}-{to_date}). Check file for reason.')
            return driver, False
        print('Data is ready to export')
    except TimeoutException:
        print('Load took too much time. There may be no results for this time period')

    # once page loads, click on export results button
    try:
        export_button = driver.find_element_by_id('btnExportResults')
        export_button.click()

        print(f'Exporting results for timeframe({from_date}-{to_date})....')
        hidden_element = driver.find_element_by_xpath('/html/body/div[5]')
        while True:
            if hidden_element.is_displayed():
                continue
            else:
                print('Results exported...')
                break

    except Exception as e:
        print('There are no result. The follow error was thrown', e)

    return driver, True


def parse_cmpgn_doc_data(results_page, year):
    soup = bs(results_page, 'lxml')
    table = soup.table
    header = [i.text for i in table.find_all('th')]
    table_rows = table.find_all('tr')
    base_url = 'https://cf.ncsbe.gov'
    all_rows = []
    for rows in table_rows:
        row = []
        for i in rows.find_all('td'):
            if i.text == ' IMAGE ' or i.text == ' DATA ':
                row.append(f'{base_url}{i.find("a").get("href")}')
            elif i.text == '\xa0':
                row.append('')
            else:
                row.append(i.text)
        if not row:
            row = header
        all_rows.append(row)
    with open(f'{current_dir}/data/{year}-cmpgn-doc.csv', 'w') as csv_output:
        write = csv.writer(csv_output)
        write.writerows(all_rows)


def append_pdf_link_to_csv(old_file, pdf_list):
    if os.path.exists(f'{current_dir}/data/{old_file}'):
        with open(f'{current_dir}/data/{old_file}', 'r') as csv_input:
            new_file = old_file.replace(' ', '-')
            with open(f'{current_dir}/data/{new_file}', 'w') as csv_output:
                writer = csv.writer(csv_output)
                reader = csv.reader(csv_input)

                all_rows = []
                row = next(reader)
                row.append('PDF Links')
                all_rows.append(row)

                for index, row in enumerate(reader):
                    row.append(pdf_list[index])
                    all_rows.append(row)

                writer.writerows(all_rows)


def pull_committee_data(year: str):
    """
    Pull campaign committee data by locating check boxes, determining if it is a report or doc, checking box, finding
    search button, waiting for download link to become available, and clicking on download link.
    var type: string: the type of document that is being searched for
    """
    driver = create_driver()
    driver.get('https://cf.ncsbe.gov/CFDocLkup/')

    # document download, need a report download too
    for doc_type in ['Document']:
        for x in range(1, 50):  # 1-45 document, 46-81 report
            checkbox = driver.find_element_by_xpath(f"/html/body/div[2]/div[2]/div/form/div/div/div/div[2]/div[2]/"
                                                    f"div/table/tbody/tr[{x}]/td[1]")
            checkbox_text = driver.find_element_by_xpath(f"/html/body/div[2]/div[2]/div/form/div/div/div/div[2]/"
                                                         f"div[2]/div/table/tbody/tr[{x}]/td[2]").text
            if doc_type in checkbox_text:
                checkbox.click()
            else:
                break

        try:
            select = Select(driver.find_element_by_id('YearList'))
            select.select_by_visible_text(year)
        except NoSuchElementException:
            print('Data can not be pulled.')
            driver.close()
            sys.exit()

        search_button = driver.find_element_by_id('btnSearch')
        search_button.click()
        # print('Searching...')
        #
        # try:
        #     WebDriverWait(driver, 160).until(ec.presence_of_element_located((By.LINK_TEXT, 'Export list to .CSV')))
        #     print('Data is ready to export')
        # except TimeoutException:
        #     print('Load took too much time.')

        # time.sleep(randint(10, 20))
        # Looking for the number of results to determine the number resources I need to gather
        # test = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div/div/div[1]").text
        # number = re.findall(r'\d+', test)
        # print(f'There are {number} links that need to be harvested')
        # pdf_links = [link.get_attribute('href') for link in driver.find_elements_by_link_text('IMAGE')]
        # print(pdf_links)

        # Export committee csv
        # export_link = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/form/div/div/div[1]/center/a")
        # export_link.click()
        # time.sleep(randint(4, 10))
        # old_file = f'{year} document list.csv'
        # append_pdf_link_to_csv(old_file, pdf_links)
    # This prints a list per row. Needs to be written to a csv
    parse_cmpgn_doc_data(driver.page_source, year)


pull_committee_data('2018')  # still need to pull this year, ran into a website error. Probably the size of the search
# request

# historic_finance_pull('1980')
# d, has_f = pull_finance_data('04/01/1988', '04/30/1988')
# if has_f:
#     d.close()
#     rename_file('04/01/1988', '04/30/1988')

