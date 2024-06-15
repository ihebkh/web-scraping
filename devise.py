#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://fr.finance.yahoo.com/devisas/'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


# In[2]:


divise = soup.find('div', class_='Pos(r) Maw($newGridWidth) Miw(a)!--tab768 Miw(a)!--tab1024 Miw(a)!--mobp Miw(a)!--mobl Miw(a)!--mobxl Bxz(bb) Bdstartc(t) Bdstartw(20px) Bdendc(t) Bdends(s) Bdstarts(s) Bxz(bb) Mx(a) Mb(40px)')
print(divise)


# In[5]:


specifique = divise.find('div', class_='Ovx(a) Ovx(h)--print Ovy(h) W(100%)')
print(specifique)


# In[48]:


table = specifique.find('table', class_='W(100%)')
print(table)


# In[65]:


data_rows = []

# Parcourir toutes les lignes du tableau
for row in table.find_all('tr')[1:]:  # ajustez l'index selon si la première ligne est un en-tête ou non
    cells = row.find_all('td')  # ou 'th' si nécessaire pour les en-têtes
    data = [cell.text.strip() for cell in cells]  # Extraire le texte de chaque cellule
    data_rows.append(data)  # Ajouter la liste des données de la ligne à la liste des données

# Convertir la liste des données en DataFrame pandas
df = pd.DataFrame(data_rows)

# Optionnel : nommer les colonnes du DataFrame si nécessaire
df.columns = ['Symbole', 'Nom' , 'Derniere Cours' , 'Variation' , '% variation' , 'NomColonne2' , 'NomColonne2']
df = df.drop(columns='NomColonne2')

# Sauvegarder le DataFrame dans un fichier Excel
df.to_excel('divise.xlsx', index=False)  # `index=False` pour ne pas inclure l'index du DataFrame dans le fichier


# In[ ]:




