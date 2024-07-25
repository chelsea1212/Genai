# -*- coding: utf-8 -*-
"""Untitled20.ipynb

Automatically generated by Google Colab.

Original file is located at
    https://colab.research.google.com/drive/15LywcHJ4WZMKmGECyqSpKZbcfXSk-RUN
"""

import nltk

nltk.download('stopwords')

import pandas as pd
import re
from bs4 import BeautifulSoup

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = nltk.corpus.stopwords.words('english')
def clean_text(text):
    if isinstance(text, str):
        text = BeautifulSoup(text, "lxml").text
        text = text.lower()
        text = REPLACE_BY_SPACE_RE.sub(' ', text)
        text = BAD_SYMBOLS_RE.sub('', text)
        text = ' '.join(word for word in text.split() if word not in STOPWORDS)
        return text
    return ""


train_file_path = 'Train.csv'
test_file_path = 'Test.csv'

train_df = pd.read_csv(train_file_path)
test_df = pd.read_csv(test_file_path)

train_df['headline'] = train_df['headline'].apply(clean_text)
train_df['description'] = train_df['description'].apply(clean_text)
train_df['text'] = train_df['headline'] + " " + train_df['description']

test_df['headline'] = test_df['headline'].apply(clean_text)
test_df['description'] = test_df['description'].apply(clean_text)
test_df['text'] = test_df['headline'] + " " + test_df['description']

train_df.to_csv('cleaned_train_data.csv', index=False)
test_df.to_csv('cleaned_test_data.csv', index=False)

print("Data preparation is complete. Cleaned data is saved to 'cleaned_train_data.csv' and 'cleaned_test_data.csv'.")

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
train_df = pd.read_csv('cleaned_train_data.csv')
test_df = pd.read_csv('cleaned_test_data.csv')

X_train, X_val, y_train, y_val = train_test_split(train_df['text'], train_df['category'], test_size=0.2, random_state=42)

svm = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', LinearSVC()),
])
svm.fit(X_train, y_train)

y_val_pred = svm.predict(X_val)

print('Accuracy on validation set: %s' % accuracy_score(y_val_pred, y_val))
print(classification_report(y_val, y_val_pred))

svm.fit(train_df['text'], train_df['category'])

y_test_pred = svm.predict(test_df['text'])

test_df['predicted_category'] = y_test_pred
test_df.to_csv('predicted.csv', index=False)

print("Predictions are made and saved to 'predicted.csv'.")

