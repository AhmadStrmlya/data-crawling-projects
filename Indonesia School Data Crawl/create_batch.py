from requests import get
from bs4 import BeautifulSoup
import time
from IPython.display import clear_output
import json

base_url = 'https://dapo.dikdasmen.kemdikbud.go.id/rekap/'
url_prov = '{}progres-sma?id_level_wilayah=0&kode_wilayah=000000&semester_id=20191'
url_kabu = '{}progres-sma?id_level_wilayah=1&kode_wilayah={}&semester_id=20191'
url_keca = '{}progres-sma?id_level_wilayah=2&kode_wilayah={}&semester_id=20191'
url_sma  = '{}progresSP-sma?id_level_wilayah=3&kode_wilayah={}&semester_id=20191'

def extract_json(url):
    try: 
        html = get(url).text
    except:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
        print('Request Failed at time: ' + current_time)
        time.sleep(5)
        return extract_json(url)
    else:
        try:
            data = json.loads(html)
            return data
        except:
            time.sleep(5)
            return extract_json(url)
        
json_prov = extract_json(url_prov.format(base_url))
data_sekolah_id = []
data_count = 0
for data_prov in json_prov:
    json_kabu = extract_json(url_kabu.format(base_url,data_prov['kode_wilayah'].strip()))
    
    for data_kabu in json_kabu:
        json_keca = extract_json(url_keca.format(base_url,data_kabu['kode_wilayah'].strip()))
        
        for data_keca in json_keca:
            data_sekolah_id.extend(extract_json(url_sma.format(base_url,data_keca['kode_wilayah'].strip())))
            print(len(data_sekolah_id))
            
with open('School_Id.txt', 'w') as f:
    for item in  data_sekolah_id:  
        f.write("%s\n" % item['sekolah_id_enkrip'])

f = open("screp.txt", "r")

data_1 = []
data_2 = []
index = 0
for x in f:
    
    # reset index to 0
    if index == 2:
        index = 0
    
    # divide the data into 2 batch
    if index == 0:
        data_1.append(x)
    elif index == 1:
        data_2.append(x)
        
    index += 1

with open('batch_1.txt', 'w') as f:
    for item in data_1:
        f.write("%s\n" % item.strip())

with open('batch_2.txt', 'w') as f:
    for item in data_2:
        f.write("%s\n" % item.strip())