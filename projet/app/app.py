
from flask import Flask, jsonify, request, render_template

# from flask import  redirect, flash

import joblib
from flask_bootstrap import Bootstrap

import pandas
import pandas as pd
import sklearn

import re
import numpy as np

import folium

import sys

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
            name, lat, lon = d['name'], float(d['lon']), float(d['lat'])
            
            # break
        
    
    return name, lat, lon


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
        station_id = request.form['stationquery']

        time_str = request.form['namequery']   
        if time_str == '':
            time_str = "2023-03-23T12:00"

#
        # station_int=11437761399
        if station_id =='':
            station_id='11437761399'
        station_int=int(station_id)
        
        name, lat, lon = get_station_info(station_info, station_int)
        
        
        #Rajouter une version dans le fichier du modèle, peut-être? Certaines fonctions
        # (format_predict_input) sont écrites pour un ensemble de features spécifique.
        model_name='velib_model_11437761399.joblib.z'
        # model_name='velib_model_'+station_id+'.joblib.z'
        # model = joblib.load("model/"+model_name)
        model = model_dict[station_int]
        
#

        # On récupère le champ namequery du template index
        # format : text="2023-03-23T12:00"
        time_str = request.form['namequery']   
        if time_str == '':
            time_str = "2023-03-23T12:00"
            
            # flash('Please enter some input.')
            # return redirect(request.url)
            
        x_test=format_predict_input(station_id, lat, lon, time_str)
        classif=predict_occup(model,x_test)
        
        my_list=[(name, station_id, str(0), classif, "", ""),
                  (name, station_id, str(0), classif, "", ""),
                  (name, station_id, str(0), classif, "", "")]
        
        # Render the response in the result.html template
        return render_template('index.html', my_list=my_list, hour1=time_str[11:16])
                               


    #This is called by the reset button on index.html. Used for tests.
    elif request.method == 'GET':
        return render_template('index.html')


    else :
        return render_template('index.html')



@app.route("/iframe")
def iframe():
    """Embed a map as an iframe on a page."""
    m = folium.Map(location=[48.856614, 2.3522219], 
        zoom_start=12, )

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"

    # for k,v in station_info.iterrows():
    for v in station_info:
        # if not v['station_id'] in [1062223873, 85008390, 653197324, 216039437, 653123610] :
            # continue

        folium.CircleMarker(
            # location = [v.lat, v.lon],
            location = [v['lat'], v['lon']],
            # color = "#000000",
            weight = 2,
            # fill_color = red(abs(v.y_test/100)).hex,
            fill_opacity = 1.0,
            # popup = str(v.y_test) + " % ",
            popup = "Station "+str(v['station_id']),
            radius = 5
        ).add_to(m)


    iframe = m.get_root()._repr_html_()

    return render_template( 'index.html' ,    iframe=iframe     )







# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    
