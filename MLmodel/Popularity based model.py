from google.colab import files
uploaded = files.upload()

# IMDB rating based model


import pandas as pd
import numpy as np
import io

df = pd.read_csv(io.BytesIO(uploaded['moviedataset.csv']))

data = pd.DataFrame(df,columns=['Title','Genre','IMDB rating','No_of_Rating'])

df['No_of_Rating'] = pd.to_numeric(df['No_of_Rating'],errors='coerce')

rating_mean=df['IMDB rating'].mean()
m= df['No_of_Rating'].quantile(0.5)

q_movies = df.copy().loc[df['No_of_Rating'] >= m]
q_movies.shape

def weighted_rating(x, m=m, rating_mean=rating_mean):
    v = x['No_of_Rating']
    R = x['IMDB rating']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * rating_mean)

q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
q_movies = q_movies.sort_values('score', ascending=False)

q_movies[['Title','Genre', 'No_of_Rating', 'IMDB rating', 'score']].head(5)
