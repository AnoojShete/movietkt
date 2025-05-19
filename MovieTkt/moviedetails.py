from tmdbv3api import TMDb, Movie, Discover
import requests


tmdb = TMDb()
tmdb.api_key = 'f7d8cdf5bedebe021fddbeeb8aff7e6e'  # Replace with your TMDb API key
tmdb.language = 'en'

def getMovie(movie_name):
    global movie_details
    movie = Movie()

    # Search movie by name
    search = movie.search(movie_name)

    if not search:
        return "Movie not found"

    movie_id = search[0].id
    movie_details = movie.details(movie_id)

    ## Movie info stored in variables    
    title = movie_details.title
    genres = ', '.join([g['name'] for g in movie_details.genres])  # Genres
    duration = movie_details.runtime  # Runtime
    release_date = movie_details.release_date
    rating = movie_details.vote_average
    description = movie_details.overview
    if movie_details.poster_path:
        poster_path = f"https://image.tmdb.org/t/p/w500{movie_details.poster_path}"
    else:
        poster_path = None
    director_name = None
    for crew_member in movie_details.casts.crew:
        if crew_member['job'] == 'Director':
            director_name = crew_member['name']
            break

    ##  Creating a dictionary to store all the values
    movie_info = {
        "title":title,
        "genre":genres,
        "duration":duration,
        "director":director_name,
        "releasedate":release_date,
        "rating":rating,
        "description":description,
        "poster":poster_path
        }

    image_data = requests.get(poster_path).content
    with open(f"MoviePosters\\{movie_name}_poster.jpg", "wb") as img_file:
        img_file.write(image_data)

    print(f"Poster image downloaded as {movie_name}_poster.jpg")

    return movie_info

   

movie_name = input("Enter name of a movie: ")
movie_info = getMovie(movie_name)

for key in movie_info:
    print(f"{key} - {movie_info[key]}")
