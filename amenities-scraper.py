# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:48:07 2019

@author: Sam Giampapa
"""

from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import openpyxl
import seaborn as sns
sns.set()

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
# =============================================================================
# Copy and paste the apartments.com url of specific property below within "quotations"
property_name_url = "https://www.apartments.com/the-paramount-houston-tx/3v6nttg/"
#==============================================================================

response = get(property_name_url, headers=headers)
print(response)
print(response.text[:1000])
html_soup = BeautifulSoup(response.text, 'html.parser')

response = get(property_name_url, headers=headers)
print(response)
print(response.text[:1000])


rent_roll_containers = html_soup.find_all('div', class_="tabContent active")
rent_roll = rent_roll_containers[0]
rent_roll

x = []
for table in rent_roll.find_all('td'):
    x.append({'Rent Roll': table.get_text()})

print(rent_roll)
pd.DataFrame(x)

wb = openpyxl.Workbook()
sheet = wb.get_active_sheet()
sheet.title = "Scraped Data"
wb.get_sheet_names()

from openpyxl.utils.dataframe import dataframe_to_rows
for r in dataframe_to_rows(pd.DataFrame(x), index=True, header=True):
    sheet.append(r)
# =============================================================================
# Replace the text within 'quotes' to the desired excel file name. don't forget .xlsx at the end
wb.save('waterford.xlsx')
#==============================================================================
