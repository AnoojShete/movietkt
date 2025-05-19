import requests

def get_currently_running_movies(api_key):
    url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=en-US&page=1"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data['results']  # Returns a list of currently running movies
    else:
        print(f"Error: {response.status_code}")
        return []

# Replace 'your_api_key_here' with your actual TMDb API key
api_key = 'your_api_key_here'
movies = get_currently_running_movies(api_key)

# Display movie titles and other relevant details
for movie in movies:
    print(f"Title: {movie['title']}")
    print(f"Release Date: {movie['release_date']}")
    print(f"Overview: {movie['overview']}")
    print(f"Poster: https://image.tmdb.org/t/p/w500{movie['poster_path']}")
    print("-" * 40)
