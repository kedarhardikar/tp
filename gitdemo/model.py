import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
nltk.download('stopwords')
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv('Train_set')
df.drop('Unnamed: 0', inplace = True, axis = 1)
df.loc[df["label"] == "real", "label"] = 1
df.loc[df["label"] == "fake", "label"] = 0

def text_process(message):
    """
    1. Remove punctuation
    2. Remove stopwords
    3. Return list of clean words
    """
    
    nopunc = [char for char in message if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    
    return [word.lower() for word in nopunc.split() if word.lower() not in stopwords.words('english')]

def listToString(s):

    string = ' '.join(s)

    return string


df['tweet'] = df['tweet'].apply(text_process)
df['tweet'] = df['tweet'].apply(listToString)

df['length'] = df['tweet'].apply(len)

y = df['label']
y=y.astype('int')

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer())
])

pipeline.fit(df['tweet'])
X_train_transformed = pipeline.transform(df['tweet'])

model_MNB = MultinomialNB()
model_MNB.fit(X_train_transformed,y)

test = pd.read_csv('Test_set')

test.drop('Unnamed: 0', inplace = True, axis = 1)


test.loc[test["Label"] == "real", "Label"] = 1
test.loc[test["Label"] == "fake", "Label"] = 0

y_test = test['Label']
test.drop('Label', inplace = True, axis = 1)

test['length'] = test['tweet'].apply(len)
test['tweet'] = test['tweet'].apply(text_process)
test['tweet'] = test['tweet'].apply(listToString)

X_test_transformed = pipeline.transform(test['tweet'])

pred_MNB = model_MNB.predict(X_test_transformed)

y_test = y_test.to_numpy(dtype ='float32')
print(classification_report(y_test,pred_MNB))

import pickle

# Save preprocessing pipeline
with open("pipeline.pkl", "wb") as f:
    pickle.dump(pipeline, f)

# Save trained model
with open("model.pkl", "wb") as f:
    pickle.dump(model_MNB, f)

print("Training complete. Model and pipeline saved.")

