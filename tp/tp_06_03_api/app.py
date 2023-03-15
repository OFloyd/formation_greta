
from flask import Flask, jsonify, request, render_template
import joblib
from flask_bootstrap import Bootstrap


app = Flask(__name__, template_folder='templates')
bootstrap=Bootstrap(app)

# 0 - hate speech 1 - offensive language 2 - neither
Labels = ["Hate speech", "Offensive language", "Neither"]
clf = joblib.load("model/hatespeech.joblib.z")

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # On récupère le champ namequery du template index
    texte = request.form['namequery']

    # On génère une prédiction et on la met au format du champ
    # probas du template result
    prediction = clf.predict_proba([texte])[0]
    # prediction = [0.1,0.4,0.5]

    # Render the response in the index.html template
    return render_template('result.html', probas=prediction)

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    
