from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel
import string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from dotenv import load_dotenv
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from github import Github
import os,requests,json
from logging.handlers import RotatingFileHandler
from time import strftime
import logging
import traceback


app = Flask(__name__)
CORS(app)

#Dot env added
APP_ROOT = os.path.dirname(__file__)   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

#SQLalchemy
app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Flask admin panel
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='Team Tomato Movie', template_mode='bootstrap3')

#Flask admin model views
#admin.add_view(ModelView(Model_Name, db.session))


# Root
@app.route('/')
def root():
    return "Welcome to Team-Tomato movie recommendation system"

# Movie cosine API
@app.route('/api/v1/movie/cosine', methods=['GET'])
def cosineSimilarityModel():
    try:
    	# cosine_str = 
        movie_user_likes = string.capwords(request.args.get('search_str'))
        df2 = pd.DataFrame(pd.read_csv('dataset/moviedataset.csv'), columns=['imdbID', 'Title', 'Genre', 'Plot', 'IMDB rating'])
        features = ['Title', 'Genre', 'Plot', 'IMDB rating']
        for feature in features:
            df2[feature] = df2[feature].fillna('')

        df2["combined_features"] = df2.apply(
            lambda row: row["Title"] + " " + row["Plot"] + " " + row["Genre"] + str(row["IMDB rating"]), axis=1)
        count_matrix = CountVectorizer().fit_transform(df2["combined_features"])
        cosine_sim = cosine_similarity(count_matrix)

        similar_movies = list(enumerate(cosine_sim[df2[df2.Title == movie_user_likes]["imdbID"].values[0]]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

        lst = []
        for i in range(0, 5):
            lst.append(df2[df2.imdbID == sorted_similar_movies[i][0]]["Title"].values[0])
        return jsonify(lst)
    except:
        return "No results found"

@app.route('/api/v1/movie/genre', methods=['GET'])
def genreBased():
    try:
        language = string.capwords(request.args.get('language'))
        genre = string.capwords(request.args.get('genre'))
        df1 = pd.read_csv('dataset/moviedataset.csv')
        data = pd.DataFrame(df1, columns=['Title', 'Genre', 'IMDB rating', 'No_of_Rating', 'Language'])
        data= data.copy().loc[data['Language'] ==language]
        df = data.copy().loc[data['Genre'] ==genre]
        df['No_of_Rating'] = pd.to_numeric(df['No_of_Rating'], errors='coerce')

        rating_mean = df['IMDB rating'].mean()
        m = df['No_of_Rating'].quantile(0.5)

        q_movies = df.copy().loc[df['No_of_Rating'] >= m]

        def weighted_rating(x, m=m, rating_mean=rating_mean):
            v = x['No_of_Rating']
            R = x['IMDB rating']
            # Calculation based on the IMDB formula
            return (v / (v + m) * R) + (m / (m + v) * rating_mean)

        q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
        q_movies = q_movies.sort_values('score', ascending=False).head(5)
        lst = [i for i in q_movies['Title']]
        return jsonify(lst)
    except Exception as e:
        return "No result found"

@app.route('/api/v1/movie/rating')
def ratingBased():
    try:
        df = pd.read_csv('dataset/moviedataset.csv')
        data = pd.DataFrame(df, columns=['Title', 'Genre', 'IMDB rating', 'No_of_Rating'])
        df['No_of_Rating'] = pd.to_numeric(df['No_of_Rating'], errors='coerce')

        rating_mean = df['IMDB rating'].mean()
        m = df['No_of_Rating'].quantile(0.5)

        q_movies = df.copy().loc[df['No_of_Rating'] >= m]
        q_movies.shape

        def weighted_rating(x, m=m, rating_mean=rating_mean):
            v = x['No_of_Rating']
            R = x['IMDB rating']
            # Calculation based on the IMDB formula
            return (v / (v + m) * R) + (m / (m + v) * rating_mean)

        q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
        q_movies = q_movies.sort_values('score', ascending=False).head(5)
        lst = [i for i in q_movies['Title']]
        return jsonify(lst)
    except Exception as e:
        return "No result found"


@app.route("/api/v1/github/contributors", methods=["GET"])
def getRepoDetails():
    g = Github()
    details=[]
    try:
        pulls=0
        commits=0
        conts=0
        print("start")
        for repo in g.get_user(os.getenv("GITHUB_USER_NAME")).get_repos():
            repo1 = g.get_repo(repo.full_name)
            pulls += repo1.get_pulls().totalCount
            commits += repo1.get_commits().totalCount
            conts += repo1.get_contributors().totalCount
        details.append(dict([("Name: ", "Team-Tomato"), ("Pull Requests: ", pulls), ("Commits: ", commits), ("Contributors: ", conts)]))
        return jsonify(details)
    except Exception as e:
        return(str(e))

@app.after_request
def after_request(response):
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s ',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500

if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=5)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)
    logger.addHandler(handle
    app.run()
