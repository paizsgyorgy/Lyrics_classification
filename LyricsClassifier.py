import pandas as pd
import spacy
import re
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

## Import the already cleaned up data from the corpus.csv
corpus_df = pd.read_csv('Output/corpus.csv', index_col=0)
y = corpus_df['Label']
X = corpus_df['Corpus']

## Make scikit learn pipeline
p = make_pipeline(CountVectorizer(),TfidfTransformer(),MultinomialNB(alpha=5))

## Fit entire pipeline
model = p.fit(X, y)
score = p.score(X, y)

print(f'The model is trained with an internal training score of {round(score,2)}')

user_input = ''

while True:
    user_input = [input('\nProvide some text to be categorized or type \'q\' and hit enter to quit the program: ')]
    if user_input == ['q']:
        print('\nQuitting program...')
        break
    y_pred = model.predict(user_input)
    prob = round(model.predict_proba(user_input).max(),2) * 100
    print()
    print(f'\nMy prediction for your input "{user_input[0]}" is that it is from artist {y_pred[0]} with a probability score of {prob}%')
