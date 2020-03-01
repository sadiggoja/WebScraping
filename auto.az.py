# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 14:46:49 2019

@author: Lenovo
"""
import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
#import urllib2
import re

#import pandas as pd
#data=pd.read_csv("cars2.csv")

with open("cars2.csv","w") as csv_file:
    csv_writer=writer(csv_file)
    csv_writer.writerow(['qiymet','marka','model','il','yurus','ban','kub','yanacaq','guc','suretler qutusu','oturucu','reng','veziyyet','kredit','elaqeli shexs','telefon','region','tarix','elan','tesvir','techizat','url'])




base_url="http://www.auto.az/cars/page/"
base="http://www.auto.az"


for pnumber in range(1,66):
    response=requests.get(f"{base_url}{pnumber}")
    page=BeautifulSoup(response.text,"html.parser")
    urls=page.find_all(class_="car_txt")
    print(f"page: {pnumber}")
    print(f"{len(urls)} cars found \n")
    for i in urls:
        url=i.findAll('a', attrs={'href': re.compile("/")})[0].get('href')    
        response2=requests.get(f"{base}{url}")
        telefon=''
        with open("cars2.csv","a",encoding='UTF-8') as csv_file:
            csv_writer=writer(csv_file)
            soup=BeautifulSoup(response2.text,"html.parser")
            
            par=soup.find_all(class_="eln_right")                
    
            sleep(2)
            td=par[0].find_all("td")
            
            marka=td[1].find("a").get_text()
            model=td[3].find("a").get_text()   
            il=td[5].get_text()
            yuruyus=td[7].find("b").get_text()
            ban=td[9].get_text()
            kub=td[11].get_text().split(', ')[0]
            yanacaq=td[11].get_text().split(', ')[1]
            guc=td[13].get_text()
            squtusu=td[15].get_text()
            tipi=td[17].get_text()
            reng=td[19].get_text()
            veziyyet=td[21].get_text()
            kredit=td[23].get_text()
            
            
            t=len(par[1].find_all("h2")) 
            for i in par[1].find_all("h2"):
                telefon+=i.get_text()+','
            
            
            
            tr=par[1].find_all("tr")
            #td2=tr[t].find_all("td")
            
            
            if len(tr[t].find_all("span")):
                ad=tr[t].find("span").get_text()
            else:
                ad=tr[t].find_all("td")[1].find("a").get_text()
            
            
            
            region=tr[t+1].find("a").get_text()
            tarix=tr[t+2].find_all("td")[1].get_text()
            elan=tr[t+3].find_all("td")[1].get_text()
            qiymet=soup.find_all(class_="eln_m_p clear")[0].find("b").get_text()
           
            
            if (soup.find_all(class_="eln_title")[0].get_text()=='Əlaqəli şəxs'):
                tesvir=""
                techizat=""
            elif (soup.find_all(class_="eln_title")[1].get_text()=='Əlavə təchizatlar'):
                tesvir=soup.find_all(class_="eln_desc")[0].get_text()
                techizat=soup.find_all(class_="eln_desc")[1].get_text()
            elif (soup.find_all(class_="eln_title")[0].get_text()=="Təsvir"):
                tesvir=soup.find_all(class_="eln_desc")[0].get_text()
                techizat=""
            else:
                tesvir=""
                techizat=soup.find_all(class_="eln_desc")[0].get_text() 
    
            csv_writer.writerow([qiymet,marka,model,il,yuruyus,ban,kub,yanacaq,guc,squtusu,tipi,reng,veziyyet,kredit,ad,telefon,region,tarix,elan,tesvir,techizat,url])
    print(f"The {pnumber}.  finished\n")            
            #csv_writer.writerow([marka,model,qiymet])            