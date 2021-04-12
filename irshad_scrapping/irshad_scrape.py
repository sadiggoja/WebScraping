import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
import pandas as pd

base="https://irshad.az/az/telefon-ve-plansetler/mobil-telefonlar/?sort=1&p="
irshad="https://irshad.az"

phones=[]
for page_number in range(7):
    response=requests.get(f"{base}{page_number+1}")
    page=BeautifulSoup(response.text,"html.parser")
    phone_sections=page.find_all('figure',  {'class':'pr_self'})
    for phone in phone_sections:
        url=f"{irshad}{phone.a.get('href')}"
        print(url)
        response=requests.get(url)
        phone_page=BeautifulSoup(response.text, "html.parser")
        details_page=phone_page.find(class_='product_details').find_all('article')
        details=dict()
        extras=[]
        details['Model']=phone_page.find(class_='product_block').find('span').text
        details['Qiymət']=phone_page.find(class_='product_block').find(class_='price').span.text
        for detail in details_page:
            detail_list=detail.p.text.split('\r\n')
            for detail in detail_list:
                detail=detail.replace('\n','')
                try:
                    details[detail.split(':')[0]]=detail.split(':')[1]
                except:
                    extras.append(detail)
        details['Əlavə xüsusiyyətlər']=extras
        details['link']=url
        phones.append(details)
        print('done')
        sleep(0.5)
    sleep(1)

phone_frame=pd.DataFrame(phones)
phone_frame.to_csv('irshad_phones.csv')
