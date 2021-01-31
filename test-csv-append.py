import lxml
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait, Select


driver = webdriver.Firefox()

driver.get('https://cf.ncsbe.gov/CFDocLkup/')
doc_type = 'Document'
rep_type = 'Report'
html = driver.page_source
soup = bs(html, 'lxml')
table = soup.table
table_rows = table.find_all('tr')
document_data = []
report_data = []
for row in table_rows:
    for row_data in row.find_all('td'):
        if doc_type in row_data.text:
            document_data.append(row_data.text)
            print('Document:', row_data.text.strip())
        elif rep_type in row_data.text:
            report_data.append(row_data.text)
            print('Report:', row_data.text.strip())

print(len(document_data), 'documents')
print(len(report_data), 'reports')
