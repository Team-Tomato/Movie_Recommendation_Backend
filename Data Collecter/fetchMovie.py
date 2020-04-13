import csv
import json
import requests
from requests.auth import HTTPBasicAuth

with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        movie = row[0]
        movie.replace(" ","+")

        url = "http://www.omdbapi.com/?t=" + movie + "&apikey=1cf7cfa6"
        response = requests.get(url)
        responseData = json.loads(response.text)
        if len(responseData) == 0:
            print("null")
        else:
            title = responseData['Title']
            year = responseData['Year']          
            genre = responseData['Genre']
            director = responseData['Director']
            write = responseData['Writer']
            actor = responseData['Actors']
            language = responseData['Language']
            country = responseData['Country']
            awards = responseData['Awards']
            rating = responseData['imdbRating']

            with open('result2.csv', 'a', newline='') as foptr:
                writer = csv.writer(foptr)
                writer.writerow([title,year,"",genre,director,write,actor,language,country,awards,rating])        
