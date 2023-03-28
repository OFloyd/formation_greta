
from flask import Flask, jsonify, request, render_template


import joblib
from flask_bootstrap import Bootstrap

import pandas
import pandas as pd
import sklearn
import random
import numpy as np
from math import radians, sin, cos, sqrt, asin


import folium
import sys
from colour import Color





app = Flask(__name__, template_folder='templates', )
bootstrap=Bootstrap(app)


#Fonctions et variables nécessaires à la prédiction : 

def predict_occup(model, x_test):

    # On prédit sur les données de test
    y_pred = model.predict(x_test)
    y_pred=f"{y_pred[0]:3.1f}"
  
    return y_pred


def format_predict_input(station_id: int, lat: float, lon: float, time_str: str):
    #Combines the results from various sources to format the features used for
    # the prediction in a way compatible with the prediction model.
    
    
    # 'time_str' is returned by the html page in the format "2023-03-23T12:00")
    # annee=int(time_str[:4]) #Unused for now
    # mois=int(time_str[5:7]) #Unused for now
    jour=int(time_str[8:10])
    heure=int(time_str[11:13])
    minute=int(time_str[14:16])

    # x_test=pd.DataFrame([[11437761399,2.273421,48.913017,jour, heure, minute]], 
    x_test=pd.DataFrame([[station_id,lon,lat,jour, heure, minute]], 
                        columns=['station_id','lon','lat','jour','heure','minute'])
    
    return x_test


def get_station_info(station_info: object, station_id: str):
    
    # name="Henri Barbusse - Bourguignons"
    
    name, lat, lon = 'station_not_found', 0, 0
    for d in station_info:
        if d['station_id'] == station_id : 
            name, lat, lon, cap = d['name'], float(d['lon']), float(d['lat']), int(d['capacity'])
            
            # break
        
    return name, lat, lon, cap


# lat=48.856614, lon=2.3522219
def get_iframe(lat=48.856614, lon=2.3522219, zoom=12, time_str=""):
    """Create a map as an iframe to embed on a page."""
    m = folium.Map(location=[lat, lon], 
        zoom_start=zoom )

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"

    # for k,v in station_info.iterrows():
    for v in station_info:
        # if not v['station_id'] in [1062223873, 85008390, 653197324, 216039437, 653123610] :
            # continue


        # y_test=float(get_table_line(v, time_str , ret_classif=1))
        
        folium.CircleMarker(
            # location = [v.lat, v.lon],
            location = [v['lat'], v['lon']],
            color = "#000000",
            weight = 2,
            # fill_color = red(abs(v.y_test/100)).hex,            
            # fill_color = red(abs(y_test)).hex,            
            fill_color = "#000000",
            fill_opacity = 1.0,
            # popup = str(v.y_test) + " % ",
            popup = "Station "+str(v['station_id']),
            radius = 5
        ).add_to(m)


    #Marker for the user's position
    folium.CircleMarker(
        # location = [v.lat, v.lon],
        location = [lat, lon],
        color = "#f13600",
        weight = 2,
        # fill_color = red(abs(v.y_test/100)).hex,
        fill_color = "#f13600",
        fill_opacity = 1.0,
        # popup = str(v.y_test) + " % ",
        popup = "User",
        radius = 5
    ).add_to(m)

    iframe = m.get_root()._repr_html_()

    return iframe




# Pour faire un dégradé de couleurs
# Dans cet exemple: 10 étapes pour passer du rouge au vert
red = Color("red")
colors = list(red.range_to(Color("green").hex,10))

def red(brightness):
    #print(brightness)
    brightness = min([int(round(9 * brightness)),9]) # convert from 0.0-1.0 to 0-255
    return colors[brightness]



#Compute the distance in km between two points knowing their latitudes and
# longitudes (cf wikipedia haversine formula)
def distance(lon1 :float, lat1 :float, lon2 :float, lat2 :float):
    # approximate radius of earth in km
    R = 6373.0

    # convert latitudes and longitudes from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # apply the Haversine formula to calculate the distance
    h = sin((lat2-lat1) / 2)**2 + cos(lat1) * cos(lat2) * sin((lon2-lon1) / 2)**2
    distance = 2*R*asin(sqrt( h ))
    
    return distance



#Selects the nmax stations closest to the position (lat,lon)
def get_station_close(lat :float, lon :float, nmax=5 ):
    dict_distance={}
    for station in station_info:
        dict_distance[station['station_id']]=distance(station['lon'], station['lat'], lon, lat)

    # key_list=sorted(dict_distance)[:nmax]
    key_list=[]
    for k, v in sorted(dict_distance.items(), key=lambda item: item[1])[:nmax] :
        key_list.append(k)


    selected_station=[]
    for station in station_info:
        if station['station_id'] in key_list:
            station['distance']=dict_distance[station['station_id']]
            selected_station.append(station)
        
    
    return selected_station




def get_table_line(station, time_str , ret_classif=0):
     
   
    station_int=station['station_id']
    lon=station['lon']
    lat=station['lat']
    jour=int(time_str[8:10])
    heure=int(time_str[11:13])
    minute=int(time_str[14:16])

 
    x_test=pd.DataFrame([[station_int,lon,lat,jour, heure, minute]], 
                 columns=['station_id','lon','lat','jour','heure','minute'])

 
    model = model_dict[station_int]
  
#
    #Predict the occupation percentage
    classif=predict_occup(model,x_test)
    if ret_classif :
        return classif


    name=station['name']
    station_code=station['stationCode']
    distance=station['distance']*1000
    capacity=station['capacity']
    n_avail_bikes=float(classif)*capacity/100.

    table_line=(name, station_code, f"{int(distance)} m.", int(np.round(n_avail_bikes)), capacity)
    return table_line



#Variables :
station_info=pd.read_json('stations_info.json').data[0]


model_dict = joblib.load("model/velib_model_all.joblib.z")


LABELS = ["Class 0", "Class 1","Class 2","Class 3","Class 4"]


# station_info=station_info[station_info['station_id'].isin([1062223873, 85008390, 653197324, 216039437, 653123610])]



@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':

        station_id=''
        # station_id = request.form['stationquery']
        # station_id = request.form['stationquery']

        # On récupère le champ namequery du template index
        # format : text="2023-03-23T12:00"
        time_str = request.form['namequery']   
        if time_str == '':
            time_str = "2023-03-23T12:00"
            
            
        #On n'utilisera pas une station_id en entrée mais une position de
        # l'utilisateur à base de latitude/longitude
        lat_u=random.uniform(48.8,48.9)
        lon_u=random.uniform(2.3,2.4)
        # print(lat_u, lon_u)
        selected_station=get_station_close(lat_u, lon_u)
#
        


        #We generate the list "my_list" that is used to create the tables in
        # the html by looping on each selected station
        my_list=[]
        for station in selected_station :
            my_list.append(get_table_line(station, time_str))

        
        
        # iframe=get_iframe()
        iframe=get_iframe(lat_u, lon_u, 16, time_str)
        
        # Render the response in the result.html template
        return render_template('predict.html', my_list=my_list, hour1=time_str[11:16], iframe=iframe)
                               


    #This is called by the reset button on index.html. Used for tests.
    elif request.method == 'GET':
        return render_template('index.html')


    else :
        return render_template('index.html')









# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    
