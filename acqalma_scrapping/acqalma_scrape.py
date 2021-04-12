import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
import pandas as pd


base="https://acqalma.az/restaurants"

response=requests.get(base)

page=BeautifulSoup(response.text,"html.parser")
rest_sections=page.find_all(class_='restaurant')

rests=[]
for rest_div in rest_sections:
    rest=dict()
    rest['Ad']=rest_div.find('span').text
    rest['url']=rest_div.find('a').get('href')
    rest['img']=rest_div.find('img').get('data-original')
    cuisine_prop=rest_div.find(class_='restaurant__cuisines').text.strip().split(':')
    rest[cuisine_prop[0]]=cuisine_prop[1]
    rests.append(rest)

    
rest_frame=pd.DataFrame(rests)


foods=[]

for rest in rests:
    response=requests.get(rest['url'])
    rest_page=BeautifulSoup(response.text, 'html.parser')

    categories_div=rest_page.find_all(class_='restaurant__content__menu-category')

    for category_div in categories_div:
        category=category_div.find('a').text.strip()
        foods_div=category_div.find_all(class_='menu-item__inner')
        for food_div in foods_div:
            food=dict()
            food['name']=food_div.find(class_='menu-item__title').text.strip()
            food['image']=food_div.find('img').get('data-original')
            food['price']=food_div.find('span').text
            food['restaurant']=rest['Ad']
            foods.append(food)            

    print(rest['Ad']+' is done')

    sleep(0.5)

    

food_frame=pd.DataFrame(foods)

rest_frame.to_csv('acqalma_rests.csv')

food_frame.to_csv('acqalma_foods.csv')


