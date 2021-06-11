import requests
import re
import numpy as np
import pandas as pd

master_page_url = 'https://www.pricebook.co.id/api/category/product?category_id=40&page={}'
master_price_history = 'https://www.pricebook.co.id/api/product/price_history?product_id={}'

def extract_spec(spec_list):
    spec_dict = {
        'RAM' : np.nan,
        'Resolusi Kamera' : np.nan,
        'Ukuran Layar' : np.nan,
        'Kapasitas Baterai' : np.nan
    }
    for spec in spec_list:
        spec_dict[spec['label']] = spec['value'] if spec['value'] != None else np.nan
        
    return spec_dict['RAM'], spec_dict['Resolusi Kamera'], spec_dict['Ukuran Layar'], spec_dict['Kapasitas Baterai']

def get_price_mean(price_hist):
    new = []
    used = []
    i = 0
    if len(price_hist) > 0:
        for price in price_hist:
            if i == 0:
                max_ = max(price['new']['price'] if price['new']['price'] != None else 0,
                           price['used']['price'] if price['used']['price'] != None else 0)
                min_ = min(price['new']['price'] if price['new']['price'] != None else 0,
                           price['used']['price'] if price['used']['price'] != None else 0)
            if price['new']['price'] != None:
                new.append(price['new']['price'])
                if max_ < price['new']['price']:
                    max_ = price['new']['price']
            if price['used']['price'] != None:
                new.append(price['used']['price'])
                if max_ < price['used']['price']:
                    max_ = price['used']['price']
        return np.mean(new) if len(new) > 0 else 0, np.mean(used) if len(used) > 0 else 0, max_, min_
    return 0, 0, 0, 0

def extract_page(page_num):
    page_url = master_page_url.format(str(page_num))
    print(f'url : {page_url} Processing!')
    response = requests.get(page_url)
    json_response = response.json()

    product_list_api = json_response['result']['product']

    product_list = []
    for product in product_list_api:
        product_id = str(product['product_id'])
        display_name_regex = re.search(r'(?<=alt=").*(?=")', product['image'])
        display_name = display_name_regex.group()

        get_price_history = requests.get(master_price_history.format(product_id))
        response_json_price_history = get_price_history.json()
        price_history = response_json_price_history['result']['price_history']

        new, used, max_, min_ = get_price_mean(price_history)

        RAM, ResolusiKamera, UkuranLayar, KapasitasBaterai = extract_spec(product['primary'])

        product_dict = {
            'product_name': product['product_name'],
            'brand_name': product['brand_name'],
            'RAM' : RAM,
            'ResolusiKamera' : ResolusiKamera,
            'UkuranLayar' : UkuranLayar,
            'KapasitasBaterai' : KapasitasBaterai,
            'release_date' : product['filter']['date_released'],
            'display_name' : display_name,
            'price_mean_new' : new,
            'price_mean_used' : used,
            'price_max' : max_,
            'price_min' : min_,
        }
        product_list.append(product_dict)
    print(f'url : {page_url} DONE!')
    print('\n ------------------------------------------------------------ \n')
    
    return pd.DataFrame(product_list)

column_names = [
    'product_name',
    'brand_name',
    'RAM',
    'ResolusiKamera',
    'UkuranLayar',
    'KapasitasBaterai',
    'release_date',
    'display_name',
    'price_mean_new',
    'price_mean_used',
    'price_max',
    'price_min'
]

df = pd.DataFrame(columns = column_names)

page_count = 280
for i in range(page_count):
    df = pd.concat([df, extract_page(i)])
    df.to_csv('pricebook_scrap.csv')
    
df.to_csv('pricebook_scrap.csv')
