import requests
import os
from datetime import datetime
import json
from PIL import Image
from io import BytesIO

class TMDBMovieFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
        
    def get_top_rated_movies(self, page=1):
        """Fetch top rated movies from TMDB"""
        endpoint = f"{self.base_url}/movie/top_rated"
        params = {
            "api_key": self.api_key,
            "language": "en-US",
            "page": page
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching top rated movies: {e}")
            return None

    def get_movie_details(self, movie_id):
        """Fetch detailed information for a specific movie"""
        endpoint = f"{self.base_url}/movie/{movie_id}"
        params = {
            "api_key": self.api_key,
            "language": "en-US",
            "append_to_response": "credits,release_dates"
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie details: {e}")
            return None

    def download_poster(self, poster_path, save_path):
        """Download movie poster and save it to specified path"""
        if not poster_path:
            return False
            
        try:
            response = requests.get(f"{self.image_base_url}{poster_path}")
            response.raise_for_status()
            
            # Open the image using PIL
            img = Image.open(BytesIO(response.content))
            
            # Save the image
            img.save(save_path)
            return True
        except Exception as e:
            print(f"Error downloading poster: {e}")
            return False

    def fetch_and_save_movies(self, num_pages=1, save_directory="movie_data"):
        """Fetch movies and save their data and posters"""
        # Create directories if they don't exist
        os.makedirs(save_directory, exist_ok=True)
        posters_dir = os.path.join(save_directory, "posters")
        os.makedirs(posters_dir, exist_ok=True)
        
        all_movies = []
        
        for page in range(1, num_pages + 1):
            movies_data = self.get_top_rated_movies(page)
            
            if not movies_data or 'results' not in movies_data:
                continue
                
            for movie in movies_data['results']:
                # Get detailed movie info
                movie_details = self.get_movie_details(movie['id'])
                
                if not movie_details:
                    continue
                
                # Extract relevant information
                movie_info = {
                    'id': movie['id'],
                    'title': movie['title'],
                    'overview': movie['overview'],
                    'rating': movie['vote_average'],
                    'release_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'poster_path': movie['poster_path'],
                    'genres': [genre['name'] for genre in movie_details.get('genres', [])],
                    'runtime': movie_details.get('runtime'),
                    'director': next((crew['name'] for crew in movie_details.get('credits', {}).get('crew', [])
                                   if crew['job'] == 'Director'), None),
                    'cast': [cast['name'] for cast in movie_details.get('credits', {}).get('cast', [])[:5]],
                }
                
                # Download poster
                if movie['poster_path']:
                    poster_filename = f"{movie['id']}.jpg"
                    poster_path = os.path.join(posters_dir, poster_filename)
                    movie_info['local_poster_path'] = poster_filename
                    self.download_poster(movie['poster_path'], poster_path)
                
                all_movies.append(movie_info)
        
        # Save movie data to JSON file
        json_path = os.path.join(save_directory, 'movies.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'movies': all_movies
            }, f, indent=4, ensure_ascii=False)
        
        return all_movies

def main():
    # Your TMDB API key
    API_KEY = "f7d8cdf5bedebe021fddbeeb8aff7e6e"  # Replace with your actual API key
    
    # Create instance of TMDBMovieFetcher
    fetcher = TMDBMovieFetcher(API_KEY)
    
    # Fetch and save movies (2 pages = 40 movies)
    movies = fetcher.fetch_and_save_movies(num_pages=2)
    
    # Print summary
    print(f"\nFetched {len(movies)} movies successfully!")
    print("\nTop 5 movies by rating:")
    
    # Sort movies by rating and print top 5
    top_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)[:5]
    for movie in top_movies:
        print(f"\nTitle: {movie['title']}")
        print(f"Rating: {movie['rating']}")
        print(f"Director: {movie['director']}")
        print(f"Genres: {', '.join(movie['genres'])}")
        print(f"Runtime: {movie['runtime']} minutes")
        print("-" * 50)

if __name__ == "__main__":
    main()
