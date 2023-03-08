
from flask import Flask, jsonify, request, render_template
import joblib
from flask_bootstrap import Bootstrap

import re
import numpy as np
from tensorflow import keras
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__, template_folder='templates')
bootstrap=Bootstrap(app)


#Fonctions et variables nécessaires à la prédiction : 
max_len   =  100
INDEX_FROM=3 

word_to_id = keras.datasets.imdb.get_word_index()
word_to_id = {k:(v+INDEX_FROM) for k,v in word_to_id.items()}
word_to_id["<PAD>"] = 0
word_to_id["<START>"] = 1
word_to_id["<UNK>"] = 2
word_to_id["<UNUSED>"] = 3


def predict_class(model, x_test):

    # On prédit sur les données de test
    y_hat = model.predict(x_test)

    # On tranforme les prédictions en labels
    i_pos = [i for i in range(len(y_hat)) if y_hat[i]>0]
    i_neg = [i for i in range(len(y_hat)) if y_hat[i]<=0]

    y_pred   = np.zeros(len(y_hat))
    y_pred[i_pos] = 1
    y_pred[i_neg] = 0
    return y_pred

def encode_txt(txt) :
    txt=re.sub(r"[^a-zA-Z'-]", ' ', txt)
    res=[ word_to_id.get(i.lower(), 2) for i in txt.split()]
    res=np.asarray(res)
    res=res.reshape((1,res.shape[0]))
    res=pad_sequences(res, maxlen=max_len, truncating='post')
    return res



# 0 - hate speech 1 - offensive language 2 - neither
Labels = ["negative comment", "positive comment"]
model = joblib.load("model/rnn_sentiment.joblib.z")


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # On récupère le champ namequery du template index
    texte = request.form['namequery']

    texte2=encode_txt(texte)
    res=predict_class(model, texte2)

    classif=Labels[int(res[0])]

    

    # Render the response in the result.html template
    return render_template('result.html', classif=classif)

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    
