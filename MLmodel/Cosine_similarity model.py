# Upload file in colab

from google.colab import files
uploaded = files.upload()

# Cosine similarity model

import io
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv(io.BytesIO(uploaded['moviedataset.csv']))
df2=pd.DataFrame(df,columns=['imdbID','Title','Genre','Plot','IMDB rating'])
features = ['Title','Genre','Plot','IMDB rating']

def combine_features(row):
    return row["Title"]+" "+row["Plot"]+" "+row["Genre"]+str(row["IMDB rating"])

for feature in features:
    df2[feature] = df2[feature].fillna('')


df2["combined_features"] = df2.apply(combine_features,axis=1)
cv = CountVectorizer()
count_matrix = cv.fit_transform(df2["combined_features"])
cosine_sim = cosine_similarity(count_matrix)    

def get_title_from_index(index):
  title=df2[df2.imdbID == index]["Title"].values[0]
  return title

def get_index_from_title(title):
    return df2[df2.Title == title]["imdbID"].values[0]

movie_user_likes = "Oh My Kadavule"

movie_index = get_index_from_title(movie_user_likes)

similar_movies = list(enumerate(cosine_sim[movie_index]))
sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

i=0

print("Top 5 similar movies to "+movie_user_likes+" are:\n")
for element in sorted_similar_movies:
    print(get_title_from_index(element[0]))
    i=i+1
    if i>=5:
        break
