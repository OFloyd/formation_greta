#!/usr/bin/env python
# coding: utf-8

import requests
import json
import pandas as pd
# import conf as cf


def dlaltitude(lat, lon):
    """
        Download altitude data from googlemaps
    """
    key="AIzaSyC7EZ27RvowjVJOohWVca_JfXoaDg2ElhI"
    base_url=f"https://maps.googleapis.com/maps/api/elevation/json?key={key}&locations={lat},{lon}"
    
    data_dict = requests.get(base_url).json()
    
    alt=data_dict["results"][0]["elevation"]
    resolution=data_dict["results"][0]["resolution"] #Inutilisé
    return alt

#Load station data
station_info=pd.DataFrame(pd.read_json('F:/work/download/stations_info.json').data.stations)

#Write a dictionary of the altitudes with the station_id as a key
dict_altitude={}
for k,v in station_info.iterrows() : 
    alt=dlaltitude(v['lat'],v['lon'])
    dict_altitude[v['station_id']]=alt

#Writes the dictionary
with open("altitude.json", "w",encoding="utf-8") as file:
    json.dump(dict_altitude, file)

