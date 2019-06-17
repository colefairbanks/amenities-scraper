from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import openpyxl
import seaborn as sns
sns.set()

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
#==============================================================================
# Copy and paste the apartments.com url of specific property below within "quotations"
property_name_url = "https://www.apartments.com/mayflower-apartments-virginia-beach-va/zv501ly/"
#==============================================================================

#implements html tool, makes program seem like a human
response = get(property_name_url, headers=headers)
print(response)
print(response.text[:1000])
html_soup = BeautifulSoup(response.text, 'html.parser')
response = get(property_name_url, headers=headers)
print(response)
print(response.text[:1000])

#list of amenities
a = []
amenities_containers = html_soup.find_all('div', class_="js-viewAnalyticsSection")
amenities = amenities_containers[0]
for link in amenities.find_all('li'):
    a.append({'Amenities': link.get_text().replace('•','')})

#opens excel and adds list of amenities
wb = openpyxl.Workbook()
sheet = wb.get_active_sheet()
sheet.title = "Scraped Data"
from openpyxl.utils.dataframe import dataframe_to_rows
for r in dataframe_to_rows(pd.DataFrame(a), index=True, header=True):
    sheet.append(r)

#Replace the text within 'quotes' to the desired excel file name. don't forget .xlsx at the end
wb.save('mayflower.xlsx')
