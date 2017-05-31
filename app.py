# -*- coding: utf-8 -*-

import pandas as pd
from shapely.geometry import Point, shape

from flask import Flask
from flask import render_template
import json

import os
import psycopg2
import urlparse
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse("postgres://robertcrozier:password@localhost:5432/postgres")
conn = psycopg2.connect(database=url.path[1:],
user=url.username,
password=url.password,
host=url.hostname,
port=url.port
)



data_path = './input/'
n_samples = 300

def get_age_segment(age):
    if age <= 22:
        return '22-'
    elif age <= 26:
        return '23-26'
    elif age <= 28:
        return '27-28'
    elif age <= 32:
        return '29-32'
    elif age <= 38:
        return '33-38'
    else:
        return '39+'

def get_location(longitude, latitude, provinces_json):
    
    point = Point(longitude, latitude)

    for record in provinces_json['features']:
        polygon = shape(record['geometry'])
        if polygon.contains(point):
            return record['properties']['name']
    return 'other'


#with open(data_path + '/geojson/china_provinces_en.json') as data_file:    
#    provinces_json = json.load(data_file)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    #FLAT FILE METHOD:
    #df = pd.read_csv(data_path + 'events.csv')
    #POSTGRES METHOD: 
    df = pd.read_sql_query("select * from iot;;", conn)

    #
    #Get n_samples records
    df = df[df['longitude'] != 0].sample(n=n_samples)
  

    #top_10_brands_en = {'华为':'Huawei', '小米':'Xiaomi', '三星':'Samsung', 'vivo':'vivo', 'OPPO':'OPPO',
    #                    '魅族':'Meizu', '酷派':'Coolpad', '乐视':'LeEco', '联想':'Lenovo', 'HTC':'HTC'}

    #df['phone_brand_en'] = df['phone_brand'].apply(lambda phone_brand: top_10_brands_en[phone_brand] 
    #                                                if (phone_brand in top_10_brands_en) else 'Other')

    #df['age_segment'] = df['age'].apply(lambda age: get_age_segment(age))

    #df['location'] = df.apply(lambda row: get_location(row['longitude'], row['latitude'], provinces_json), axis=1)
    #df['location'] = 'other'
    #cols_to_keep = ['timestamp', 'longitude', 'latitude', 'phone_brand_en', 'gender', 'age_segment', 'location']
    cols_to_keep = ['timestamp', 'longitude', 'latitude', 'phone_brand_en', 'gender', 'age_segment', 'location']
    df_clean = df[cols_to_keep].dropna()
    print(df_clean)
    return df_clean.to_json(orient='records')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
