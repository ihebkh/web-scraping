from bs4 import BeautifulSoup
import requests
import pandas as pd

# Define the base URL
base_url = 'https://superiorrental.ae/Brand/luxury-cars/'

# Initialize an empty list to store all car entries
all_car_entries = []

# Loop through pages
for page_number in range(1, 8):  # Assuming there are 5 pages, adjust as needed
    # Construct the URL for each page
    url = f'{base_url}?page={page_number}'

    # Make a request to the current page
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Find and store car entries for the current page
    cars_container = soup.find('ul', class_='products elementor-grid columns-3')
    if cars_container:
        car_entries = cars_container.find_all('div', class_='elementor elementor-22045')
        all_car_entries.extend(car_entries)
        print(f"Page {page_number} processed")
    else:
        print(f"No car entries found on page {page_number}")

car_data = {'Type': [], 'date fabrication': []}
for car_entry in all_car_entries:
    car_title_element = car_entry.find('h3', class_='product_title entry-title elementor-heading-title elementor-size-large')
    car_title = car_title_element.text.strip()
    car_data['Type'].append(car_title)

    car_details_element = car_entry.find('div', class_='elementor-widget-wrap elementor-element-populated')
    datefabrication = car_details_element.text.strip()
    datefabrication = datefabrication.replace(car_title, '').strip()
    car_data['date fabrication'].append(datefabrication)

df = pd.DataFrame(car_data)

df[['Type', 'Model']] = df['Type'].str.split(n=1, expand=True)
df[['date fabrication', 'horsepower','places','typedelocation','typedelocation2','price','AED','day','others']] = df['date fabrication'].str.split(n=8, expand=True)
df = df[['Type', 'Model', 'date fabrication','horsepower','places','typedelocation','typedelocation2','price','AED','day']]

df = df.drop(columns='typedelocation')
df = df.drop(columns='typedelocation2')
df = df.drop(columns='AED')
df = df.drop(columns='day')
column_to_update = 'price'

# Add "$" to the beginning of each value in the specified column
df[column_to_update] =  df[column_to_update].astype(str) +'$' 




df.to_excel('dubai3.xlsx', index=False)

print("Data exported to dubai3.xlsx")