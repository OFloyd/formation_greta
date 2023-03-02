#!/usr/bin/env python
# coding: utf-8


# Initialisation de flask / Génération du 'site'

from flask import Flask, jsonify, request, render_template
import joblib

from flask_bootstrap import Bootstrap


app = Flask(__name__)


clf=joblib.load("./model/hatespeech.joblib.z")


# texts = [
#     {
#         'text_in': ''
#     }
# ]

@app.route('/')
def get_root() :
    return 'Hello world'
    # return render_template('/home/stagiaire/formation_greta/tp/tp_api/templates/index.html')
    # return render_template('templates/index.html')
    # return render_template('index.html')



@app.route('/predict', methods=['GET'])
def predict() :
 
    text=request.json["text"]
    
    out=clf.predict_proba([text])

    return jsonify(out.tolist())

    # return jsonify(out.tolist())


# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
