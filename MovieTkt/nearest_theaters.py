import requests
from math import radians, sin, cos, sqrt, atan2

import requests

def get_lat_long_osm(location):
    # OSM Nominatim API endpoint
    url = "https://nominatim.openstreetmap.org/search"
    
    # Define the parameters for the request
    params = {
        'q': location,  # Location to search
        'format': 'json',  # Response format
        'limit': 1  # Limit to the first result
    }
    
    # Set a custom user-agent to identify your application
    headers = {
        'User-Agent': 'MyGeocodingApp/1.0 (randacc0008@gmail.com)'  # Custom user agent
    }
    
    # Make the request to the OSM Nominatim API
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            return None, None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None

# Example usage
if __name__ == "__main__":
    location = input("Enter your place: ")
    lat, lon = get_lat_long_osm(location)
    
    if lat and lon:
        print(f"Latitude: {lat}, Longitude: {lon}")
    else:
        print("Location not found.")


class TheaterFinder:
    def __init__(self):
        self.api_url = "https://overpass-api.de/api/interpreter"

    def get_nearby_theaters(self, latitude, longitude, radius_km=10):
        radius_meters = radius_km * 1000
        query = f"""
        [out:json];
        (
          node["amenity"="cinema"](around:{radius_meters},{latitude},{longitude});
          way["amenity"="cinema"](around:{radius_meters},{latitude},{longitude});
          relation["amenity"="cinema"](around:{radius_meters},{latitude},{longitude});
        );
        out center;
        """
        
        response = requests.get(self.api_url, params={'data': query})
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        data = response.json()
        theaters = data.get("elements", [])

        nearby_theaters = []
        for theater in theaters:
            if theater['type'] == 'node':
                theater_lat, theater_lon = theater['lat'], theater['lon']
            else:  # way or relation
                theater_lat, theater_lon = theater['center']['lat'], theater['center']['lon']
            
            distance = self.haversine(latitude, longitude, theater_lat, theater_lon)
            nearby_theaters.append({
                'id': theater['id'],
                'name': theater.get('tags', {}).get('name', 'Unknown Theater'),
                'distance': round(distance, 2)
            })

        return sorted(nearby_theaters, key=lambda x: x['distance'])

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in kilometers

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance

# Example usage
if __name__ == "__main__":
    finder = TheaterFinder()

    # Get user's location (in a real app, you'd get this from a geolocation service)
    user_lat, user_lon = 19.0771, 72.9980

    # Find nearby theaters
    nearby_theaters = finder.get_nearby_theaters(float(lat), float(lon))

    print("Nearby theaters:")
    theaters = []
    for theater in nearby_theaters:
        print(f"{theater['name']} - {theater['distance']} km")
        #theaters.append(theater)
