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

property_container = html_soup.find_all('div', class_="propertyNameRow clearfix")
theProperty = property_container[0]

property_name = theProperty.find_all('h1', class_="propertyName")[0].text
print(property_name)
amenities_containers = html_soup.find_all('div', class_="js-viewAnalyticsSection")
amenities = amenities_containers[0]

rent_roll = html_soup.find_all('div', class_="tabContainer")[0].text
therent_roll = rent_roll[0]


x = []
for table in rent_roll.find_all('td'):
    x.append({'Rent Roll': table.get_text()})

print(rent_roll)

d = []
for link in amenities.find_all('li'):
    d.append({'Amenities': link.get_text().replace('•','')})

pd.DataFrame(d)

wb = openpyxl.Workbook()
sheet = wb.get_active_sheet()
sheet.title = "Scraped Data"
wb.get_sheet_names()

from openpyxl.utils.dataframe import dataframe_to_rows
for r in dataframe_to_rows(pd.DataFrame(d), index=True, header=True):
    sheet.append(r)
# =============================================================================
# Replace the text within 'quotes' to the desired excel file name. don't forget .xlsx at the end
wb.save('paramount.xlsx')
#==============================================================================

