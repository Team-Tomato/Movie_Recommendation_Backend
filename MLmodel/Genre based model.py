from google.colab import files
uploaded = files.upload()

# Genre based model

import pandas as pd
import numpy as np
import io

df = pd.read_csv(io.BytesIO(uploaded['moviedataset.csv']))

data = pd.DataFrame(df,columns=['Title','Genre','Plot'])

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')
data['Genre'] = data['Genre'].fillna('')

tfidf_matrix = tfidf.fit_transform(data['Genre'])
tfidf_matrix.shape

from sklearn.metrics.pairwise import linear_kernel

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(data.index, index=data['Title']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:6]

    movie_indices = [i[0] for i in sim_scores]
    return data['Title'].iloc[movie_indices]

get_recommendations('Oh My Kadavule')
