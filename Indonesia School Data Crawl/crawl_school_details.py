#!/usr/bin/env python
# coding: utf-8

# In[1]:


from requests import get
from bs4 import BeautifulSoup
import time
from IPython.display import clear_output
from random import randint
import json


# In[2]:


base_url = 'http://dapo.dikdasmen.kemdikbud.go.id/'
url_json = 'rekap/sekolahDetail?semester_id=20191&sekolah_id={}'
url_web  = 'sekolah/{}'


# In[3]:


def scrapPanel(content):
    list_data = []
    try:
        for cnt in content.find_all('p'):
            data = cnt.text.split(':')[1].strip()
            if (data == '-' or data == ''): data = '-'
            list_data.append(data)
    except:
        return ['']
    return list_data

def scrapPage(url):
    # test url : https://dapo.dikdasmen.kemdikbud.go.id/sekolah/F757B05AEE38F2819175
    
    url_ = get(url.strip())
    html = BeautifulSoup(url_.text, 'lxml')
    data_ = []
    
    # get school profile
    try:
        # get nama sekolah
        nama_sekolah = html.find('h2', class_='name')
        data_.append(nama_sekolah.text)
        
        # get akreditasi sekolah
        usermenu = html.find('div', class_='profile-usermenu')
        for li in usermenu.find_all('li'):
            cnt = li.find('strong').text
            data_.append(cnt)
        
        cnt_profile = html.find('div', id='profil')
        for content in cnt_profile.find_all('div', class_='panel-body'):
            data_.extend(scrapPanel(content))
        
        '''
            result from scraping school profile: 
                NPSN, status, Bentuk Pendidikan, Status Kepemilikan, SK Pendirian Sekolah,
                Tanggal SK Pendirian, SK Izin Operasional, Tanggal SK Izin Operasional,
                Kebutuhan Khusus Dilayani, Nama Bank, Cabang KCP/Unit, Rekening Atas Nama,
                Luas Tanah Milik, Luas Tanah Bukan Milik, Status BOS, Waku Penyelenggaraan,
                Sertifikasi ISO, Sumber Listrik, Daya Listrik, Akses Internet
        '''

        # get contact
        cnt_contact = html.find('div', id='kontak')
        data_.extend(scrapPanel(cnt_contact))
        '''
            result from scraping contact:
                Alamat, RT/RW, Dusun, Desa/Kelurahan, Kecamatan, Kabupaten, Provinsi,
                Kode Pos, Lintang, Bujur
        '''
        return data_
    except:
        return ['-']


# In[4]:


# stress test
def req_get(url):
    x = base_url + url_web.format(url)
    try:
        url_ = get(x)
    except:
        time.sleep(5)
        return req_get()
    else:
        return url_
    
f = open("batch_1.txt", "r")
it = 1
data = []
for x in f:
    url = base_url + url_web.format(x)
    data.append(scrapPage(url))
    print(f'req_count : {it}')
    it += 1
    
import csv

with open("batch_1.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)


# In[ ]:




