from tmdbv3api import TMDb, Movie, Discover
import requests

# Initialize TMDb with your API key
tmdb = TMDb()
tmdb.api_key = 'f7d8cdf5bedebe021fddbeeb8aff7e6e'  # Replace with your TMDb API key
tmdb.language = 'en'  # Set language to English

# Function to fetch movie details by movie ID or title
def fetch_movie_details(movie_name):
    global movie_details
    movie = Movie()
    
    # Search movie by name
    search = movie.search(movie_name)
    
    if not search:
        return "Movie not found!"
    
    # Fetch first result (most relevant one)
    movie_id = search[0].id
    movie_details = movie.details(movie_id)
    
    # Movie information
    title = movie_details.title
    genres = ', '.join([g['name'] for g in movie_details.genres])  # Genres
    duration = movie_details.runtime  # Runtime
    release_date = movie_details.release_date
    rating = movie_details.vote_average
    description = movie_details.overview
    
    # Fetching poster
    poster_path = f"https://image.tmdb.org/t/p/w500{movie_details.poster_path}" if movie_details.poster_path else "No image available"
    
    # Fetching director's name (from crew)
    director_name = None
    for crew_member in movie_details.casts.crew:
        if crew_member['job'] == 'Director':
            director_name = crew_member['name']
            break
    
    # Movie details dictionary
    movie_info = {
        "Title": title,
        "Genres": genres,
        "Duration (min)": f'{duration//60}h, {duration%60}m',
        "Director": director_name,
        "Release Date": release_date,
        "Rating": rating,
        "Description": description,
        "Poster URL": poster_path
    }
    
    return movie_info

# Example usage:
movie_name = input("Enter the movie title: ")
movie_info = fetch_movie_details(movie_name)

# Display movie details
for key, value in movie_info.items():
    print(f"{key}: {value}")

# You can also download the poster image if needed
poster_url = movie_info["Poster URL"]
if poster_url != "No image available":
    image_data = requests.get(poster_url).content
    with open(f"{movie_name}_poster.jpg", "wb") as img_file:
        img_file.write(image_data)
    print(f"Poster image downloaded as {movie_name}_poster.jpg")
