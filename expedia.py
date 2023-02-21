import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree


# ow library
import aux_text

class ExpediaMX:
    
    def __init__(self):
        print('Extracción Expedia MX')
        
        self.header     = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"}
        self.url        = "https://www.expedia.mx/Cancun-Hoteles-Seadust-Cancun-All-Inclusive-Family-Resort.h1579645.Informacion-Hotel?chkin=2023-03-04&chkout=2023-03-05&x_pwa=1&rfrr=HSR&pwa_ts=1677003894673&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5teC9Ib3RlbC1TZWFyY2g%3D&useRewards=false&rm1=a2&regionId=11186&destination=Quintana+Roo%2C+M%C3%A9xico&destType=MARKET&neighborhoodId=800022&selected=1579645&hotelName=Seadust+Canc%C3%BAn+All+Inclusive+Family+Resort&sort=RECOMMENDED&top_dp=6362&top_cur=MXN&userIntent=&selectedRoomType=321656566&selectedRatePlan=389230789"
        self.respuesta  = requests.get(self.url, headers = self.header)
        self.soup       = BeautifulSoup(self.respuesta.content, "html.parser")
        self.dom        = etree.HTML(str(self.soup))

        self.date       = time.strftime("%d/%m/%Y")
        
        self.extrac_info()
    
    
    def dowload_csv(self, data):
        print('Generando el CSV...') 
        df = pd.DataFrame(data = data)
        return df.to_csv(f'csv_file/seadust-expediaMX.csv',index = False, header=True)
    
    
    def extrac_info(self):
                

        dataset = {'nombre': [], 'conceptop': [], 'fecha_review' : [], 'critica' : [], 'review' : [], 'estadia' : [], 'date_extract' : []}
        
        list_reviews = self.dom.xpath('//div[@class="uitk-card-content-section uitk-card-content-section-border-block-end uitk-card-content-section-padded"]')

        for review_only in list_reviews:
            # print('Hola mundo')
            nombre       = review_only.xpath('.//span[@itemprop="name"]')[0].text
            conceptop    = review_only.xpath('.//div[@class="uitk-text uitk-type-300 uitk-text-default-theme"]')[0].text
            fecha_review = review_only.xpath('.//span[@itemprop="datePublished"]')[0].text
            critica      = review_only.xpath('.//span[@class="uitk-text uitk-type-200 uitk-text-default-theme uitk-spacing uitk-spacing-padding-inlinestart-two"]')[0].text
            review       = review_only.xpath('.//span[@itemprop="description"]')[0].text
            estadia      = review_only.xpath('.//div[@class="uitk-text uitk-type-200 uitk-text-default-theme uitk-layout-flex-item"]')[0].text
        
            review = aux_text.remove_newline(review)
            
            if conceptop is None:
                conceptop = 'Sin concepto'
            print(nombre)
            dataset['nombre'].append(nombre)
            dataset['conceptop'].append(conceptop)
            dataset['fecha_review'].append(fecha_review)
            dataset['critica'].append(critica)
            dataset['review'].append(review)
            dataset['estadia'].append(estadia)
            dataset['date_extract'].append(self.date)
        
        
        return self.dowload_csv(dataset)