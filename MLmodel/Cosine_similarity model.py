# Upload file in colab

from google.colab import files
uploaded = files.upload()

# Cosine similarity model

import io
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv(io.BytesIO(uploaded['Movies - Tamil.csv']))

features = ['Title','Year','Genre','Director','Writer','Actors','Language','Country','Awards','IMDB rating']

def combine_features(row):
    return row['Title'] +" "+str(row['Year'])+" "+row["Genre"]+" "+row["Director"]+" "+row['Writer']+" "+row['Actors']+" "+row['Language']+" "+row['Country']+" "+row['Awards']+" "+str(row['IMDB rating'])

for feature in features:
    df[feature] = df[feature].fillna('')

df["combined_features"] = df.apply(combine_features,axis=1)
cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)

def get_title_from_index(index):
  title=df[df.index == index]["Title"].values[0]
  genre=df[df.index == index]["Genre"].values[0]
  return title,genre

def get_index_from_title(title):
    return df[df.Title == title]["Index"].values[0]

movie_user_likes = "Pattas"

movie_index = int(get_index_from_title(movie_user_likes))

similar_movies = list(enumerate(cosine_sim[movie_index]))
sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

i=0

print("Top 5 similar movies to "+movie_user_likes+" - Genre : "+df[df.Title==movie_user_likes]["Genre"].values+" are:\n")
for element in sorted_similar_movies:
    print(get_title_from_index(element[0]))
    i=i+1
    if i>=5:
        break
