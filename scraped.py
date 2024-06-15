from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://pugachev.miami'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

cars_container = soup.find('div', class_='avia-content-slider-inner')
car_entries = cars_container.find_all('div', class_='slide-entry-wrap')

car_data = {'Car Name': [], 'Price': [], 'Details': []}

for car_entry in car_entries:
    car_title = car_entry.find('h3', class_='slide-entry-title entry-title').text.strip()
    car_price = car_entry.find('div', class_='slide-entry-excerpt entry-content').text.strip()
    car_details_element = car_entry.find('a')
    if car_details_element and 'href' in car_details_element.attrs:
        car_details_url = car_details_element['href']
        
        car_details_page = requests.get(car_details_url)
        car_details_soup = BeautifulSoup(car_details_page.text, 'html.parser')

        car_details = car_details_soup.find('div', class_='tables').text.strip() if car_details_soup else ""
    
    car_data['Car Name'].append(car_title)
    car_data['Price'].append(car_price)
    car_data['Details'].append(car_details)

df = pd.DataFrame(car_data)

# Splitting 'Details' column into separate columns
details_split = df['Details'].str.split('\s{3}', expand=True)

# Renaming the columns to represent the information
details_split.columns = [f'Detail_{i}' for i in range(len(details_split.columns))]

# Extracting information after ':'
for col in details_split.columns:
    details_split[col] = details_split[col].str.split(':').str[-1].str.strip()

# Concatenating the original DataFrame with the split details
df = pd.concat([df, details_split], axis=1)

# Dropping the original 'Details' column
df.drop(columns=['Details'], inplace=True)

df.to_excel('cars_data.xlsx', index=False)

print("Data exported to 'cars_data.xlsx'")
