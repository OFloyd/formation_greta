#!/usr/bin/env python
# coding: utf-8


# Initialisation de flask / Génération du 'site'

from flask import Flask, jsonify, request
import joblib




clf=joblib.load("./model/hatespeech.joblib.z")



text="Blabla"

out=clf.predict_proba(text)
# print(out)
    # return jsonify({out})
# print(out)
help(out)

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
