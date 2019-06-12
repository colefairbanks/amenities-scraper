from bs4 import BeautifulSoup
from requests import get
import pandas as pd
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
