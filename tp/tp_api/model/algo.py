import pandas as pd
import re
import joblib

#petit clean 
df = pd.read_csv("../data/labeled_data.csv", usecols=['class', 'tweet'])
df['tweet'] = df['tweet'].apply(lambda tweet: re.sub('[^A-Za-z]+', ' ',
                                                     tweet.lower()))

#labels 
# 0 - hate speech 1 - offensive language 2 - neither
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from stop_words import get_stop_words

#pipeline 
clf = make_pipeline(
    TfidfVectorizer(stop_words=get_stop_words('en')),
    OneVsRestClassifier(SVC(kernel='linear', probability=True))
)

#fit 
clf = clf.fit(X=df['tweet'], y=df['class'])

#test 
text = "I hate you, please die!"
clf.predict_proba([text])

#save weights 
model_filename = "hatespeech.joblib.z"
joblib.dump((clf), model_filename)