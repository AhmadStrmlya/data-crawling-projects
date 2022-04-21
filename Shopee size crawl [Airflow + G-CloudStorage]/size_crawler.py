#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
from datetime import datetime
from google.cloud import storage
import csv
import requests
import json
import re
import os

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    credential_path = 'gcs/dags/helper/manifest-setup-333302-3e5f2cbfdd1f.json'
    storage_client = storage.Client.from_service_account_json(credential_path)

    print(list(storage_client.list_buckets()))

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)

def csv_writer(data, path):
    
    with open(path, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 

        # writing the data rows 
        csvwriter.writerows(data)
        upload_to_bucket('dags/data/scrape_result.csv', path, 'asia-southeast1-airflow-env-932e6e6a-bucket')

def crawl_size():
    template = 'https://shopee.co.id/api/v4/item/get?itemid={}&shopid={}'
#     rows_format -> [['date_pulled', 'shopid', 'itemid', 'size', 'stock']]
    rows = []

    with open('gcs/dags/data/shopid_productid.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        header = next(csv_reader)
        if header != None:
            for row in csv_reader:
                link = template.format(row[1], row[0])
                page_request = requests.get(link)
                soup = BeautifulSoup(page_request.content, 'lxml')

                json_data = json.loads(soup.text)
                plist = json_data['data']['models']

                for i in range(len(plist)):
                    temp = []
                    temp.append(datetime.now())
                    temp.append(row[0])
                    temp.append(plist[i].get("itemid"))
                    x = re.findall(r'[A-Za-z]+|\d+', plist[i].get("name"))
                    temp.append(x[0])
#                     if(len(x) == 1):
#                         temp.append(x[0])
#                         temp.append("")
#                     elif(len(x) == 2):
#                         temp.append(x[0])
#                         temp.append(x[1])
#                     else:
#                         temp.append(x[0])
#                         temp.append(x[1] + " " + x[2])
#                     temp.append(plist[i].get("price")/100000)
                    temp.append(plist[i].get("stock"))
                    rows.append(temp)

    path = "gcs/dags/data/result.csv"
    csv_writer(rows, path)
    print("uploaded")
