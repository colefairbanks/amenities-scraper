from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import openpyxl
import seaborn as sns
sns.set()

headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
#==============================================================================
# Copy and paste the apartments.com url of specific property below within "quotations"
property_name_url = "https://www.apartments.com/the-waterford-morrisville-nc/yvq7spr/"
#==============================================================================

#implements html tool, makes program seem like a human
response = get(property_name_url, headers=headers)
print(response)
print(response.text[:1000])
html_soup = BeautifulSoup(response.text, 'html.parser')
response = get(property_name_url, headers=headers)
print(response)
print(response.text[:1000])

#property title
property_container = html_soup.find_all('div', class_="propertyNameRow clearfix")
theProperty = property_container[0]
property_name = theProperty.find_all('h1', class_="propertyName")[0].text.strip()
print(property_name)

#property address & city/state
address_container = html_soup.find_all('div', class_="propertyAddress")
theAddress = address_container[0]
address = theAddress.find_all('span')[0].text
city_state = theAddress.find_all('h2')[0].text.replace(" ", "").partition(",")[2]
print(address)
print(city_state)

#url address
url_container = html_soup.find_all('div', class_="linkWrapper")
theURL = url_container[0]
URL = theURL.find_all('a')[0].get('href')[0:50]
print(URL)

#list of amenities
a = []
amenities_containers = html_soup.find_all('div', class_="js-viewAnalyticsSection")
amenities = amenities_containers[0]
for link in amenities.find_all('li'):
    a.append({'Amenities': link.get_text().replace('•','')})

#unit mix
unit_mix_containers = html_soup.find_all('div', class_="tabContent active")
unit_mix = unit_mix_containers[0]
unit_mix

b = []
beds_containers = html_soup.find_all('td', class_="beds")
beds = beds_containers[0]
for column in unit_mix.find_all('span', class_='longText'):
    b.append({'Beds': column.get_text()})
    
ba = []
baths_containers = html_soup.find_all('td', class_="baths")
amenities = amenities_containers[0]
for column in unit_mix.find_all('span', class_="longText"):
    ba.append({'Baths': column.get_text()})
    
rent = []
for column in unit_mix.find_all('td', class_='rent'):
    rent.append({'Rent': column.get_text()})
    
name = []
for column in unit_mix.find_all('td', class_='name'):
    name.append({'Name': column.get_text()})
    
cols = ['Bed', 'Baths', 'Rents']

df = pd.DataFrame({'Bed': bed,
                           'Baths': bath,
                           'Rents': rent})[cols]

from openpyxl.utils.dataframe import dataframe_to_rows
dataframe_to_rows(pd.DataFrame({'Bed': bed, 'Baths': bath, 'Rents': rent})[cols])
# =============================================================================
# Replace the text within 'quotes' to the desired excel file name. don't forget .xlsx at the end
wb = openpyxl.Workbook()
sheet = wb.get_active_sheet()
wb.save('test123.xls')
sheet = wb.get_sheet_by_name('Market Survey')
sheet['G5'] = property_name
sheet['G6'] = address
sheet['G12'] = URL
#==============================================================================
