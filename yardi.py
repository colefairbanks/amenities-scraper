from selenium import webdriver
import time
from bs4 import BeautifulSoup
from requests import get
import seaborn as sns

sns.set()
headers = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

#==============================================================================
# Copy and paste the apartments.com url of specific property below within "quotations"
property_name_url = "https://www.apartments.com/the-waterford-morrisville-nc/yvq7spr/"
#==============================================================================

response = get(property_name_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
response = get(property_name_url, headers=headers)

#property address & city/state
address_container = soup.find_all('div', class_="propertyAddress")
theAddress = address_container[0]
address = theAddress.find_all('span')[0].text
city_state = theAddress.find_all('h2')[0].text.replace(" ", "").partition(",")[2].replace('\n', ' ').replace('\r', '').rstrip()
full_address = address + "," + city_state

# Using Chrome to access web
chromedriver ="/Users/colefairbanks/Documents/Yardi/chromedriver"
driver = webdriver.Chrome(chromedriver)
driver.get('https://matrix.pi-ei.com/login')

# Locate id and password
username_box = driver.find_element_by_id('Username')
password_box = driver.find_element_by_name('Password')

# Send login information
username_box.send_keys('bach.nguyen@croataninvestments.com')
password_box.send_keys("temp")

# Click login
login_button = driver.find_element_by_name('submit')
login_button.click()

#search property
time.sleep(3)
property_search_box = driver.find_element_by_id('prop_search_text')
property_search_box.send_keys(full_address)
time.sleep(3)
search_button = driver.find_element_by_class_name("autocomplete-option")
search_button.click()
search_button = driver.find_element_by_id('prop_search_btn')
search_button.click()

#select property
time.sleep(7)
property_link = driver.find_element_by_class_name('propertyTileHrefs')
property_link.click()

#grabs url for beautifulsoup to scrape
correct_tab = driver.window_handles[1]
driver.switch_to_window(correct_tab)
yardi_property_url = driver.current_url

#yardi units
for unitnum in driver.find_elements_by_class_name('propdetail_units'):
    units = unitnum.text[0:3]

#phone
phone_container = driver.find_element_by_id('propertyInformation').text.replace('\n', ' ').split("Phone ")[1]
phone = phone_container[0:14]

#owner
owner_manager_container = driver.find_element_by_class_name('company-detail').text.replace('\n', ' ').split("Owner Groups ",1)[1]
owner_container = owner_manager_container.rsplit(" (")[0].split(' ')
owner_container2 = " ".join(owner_container)

if "." in owner_container2:
   owner = owner_container2.rsplit(' ',3)[0]
else:
   owner = owner_container2.rsplit(' ',2)[0]  

#manager
owner_manager_container2 = driver.find_element_by_class_name('company-detail').text.replace('\n', ' ').split("Manager Groups ",1)[1]
manager_container = owner_manager_container2.rsplit(" (")[0].split(' ')
manager_container2 = " ".join(manager_container)

if "." in owner_container2:
   manager = manager_container2.rsplit(' ',3)[0]
else:
   manager = manager_container2.rsplit(' ',2)[0]  

#amenities
amenities_container = driver.find_element_by_id('charsAccordion').text
amenities = amenities_container.split('\n')

#year built
parcel_data_link = driver.find_element_by_partial_link_text('Parcel Data')
parcel_data_link.click()
column_info = driver.find_element_by_class_name('cols22 ').text.replace('\n',' ').split("Year built ")[1]
year_built = column_info.split(' ')[0]

#go back to home page and begin search again
time.sleep(2)
home_button = driver.find_element_by_partial_link_text('Home')
home_button.click()

#logout
logout_button = driver.find_element_by_partial_link_text('Logout')
logout_button.click()

#quit session
driver.quit()