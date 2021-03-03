import requests
import json
from pprint import PrettyPrinter
pp = PrettyPrinter()

title = raw_input("Enter movie name: ")
api_key = '94c39b02'

# validate movie name
if title == '':
    print("Invalid input entered")
    exit()

# prepare URL parameters. Use OMDB API for fetching movie details
url = 'http://www.omdbapi.com/?apikey=' + api_key
params = {
    's': title,
    'type':'movie',
    'r': 'json'
}

# API returns all movie names related to user query
res = requests.get(url, params=params)

if res.status_code != 200:
    raise ApiError('Unable to fetch data from API')

# parse result to json
jsonRes = res.json()
search_results = jsonRes.items()

if search_results[1][0] == 'Error':
    print("No movies were found related to your query")
    exit()

# get movie names found
search_results = search_results[0][1]    

print("The following movies were found related to your query:")

movie_dict = {}

# iterate through all related movie names and display the info to user
for idx, item in enumerate(search_results):
    movie =  'Movie Id: ' + str(idx) + " ,Title: " + item['Title'] + ", Year: " + item['Year']
    print(movie)
    movie_dict[idx] = item['imdbID']

# ask user to pick a movie id for which the Imdb rating needs to be found
try:
    selected_movie = int(raw_input("Enter the movie Id for which you want to find the IMDB rating: "))

    # validate input range
    if selected_movie < 0 or selected_movie > (len(search_results) - 1):
        raise Exception()
except:
    print("Invalid input entered")
    exit()

del params['s']
params['i'] = movie_dict[selected_movie]
params['plot'] = 'full'

# API returns all details of the movie selected
res = requests.get(url, params=params)

if res.status_code != 200:
    raise ApiError('Unable to fetch data from API')

# print IMDB rating of the movie
print("The IMDB rating of the movie is: " + res.json().items()[16][1])