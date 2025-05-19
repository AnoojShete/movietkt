import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from math import radians, sin, cos, sqrt, atan2

class TheaterSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Theater Search")
        self.root.geometry("800x600")
        
        self.theater_finder = TheaterFinder()
        
        # States and cities data
        self.states = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", 
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", 
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", 
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]
        self.cities = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Tirupati"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Ziro", "Pasighat", "Bomdila"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar", "Tezpur", "Jorhat"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia"],
    "Chhattisgarh": ["Raipur", "Bilaspur", "Durg", "Korba", "Rajnandgaon"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
    "Haryana": ["Gurgaon", "Faridabad", "Panipat", "Ambala", "Hisar"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Solan", "Mandi"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh"],
    "Karnataka": ["Bangalore", "Mysore", "Mangalore", "Hubli", "Belgaum"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Alappuzha"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain"],
    "Maharashtra": ["Mumbai","Pune","Nagpur","Nashik","Aurangabad","Solapur","Thane","Kolhapur","Satara","Jalna","Akola","Wardha","Amravati","Chandrapur","Bhiwandi","Kalyan","Dombivli","Ulhasnagar","Miraroad","Bhandup","Ghatkopar","Malad","Vasai","Virar","Thane","Mira-Bhayandar"
    ],
    "Manipur": ["Imphal", "Thoubal", "Churachandpur", "Bishnupur", "Ukhrul"],
    "Meghalaya": ["Shillong", "Tura", "Cherrapunji", "Jowai", "Nongpoh"],
    "Mizoram": ["Aizawl", "Lunglei", "Saiha", "Champhai", "Serchhip"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Puri", "Sambalpur"],
    "Punjab": ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner"],
    "Sikkim": ["Gangtok", "Namchi", "Gyalshing", "Mangan", "Pelling"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailashahar", "Belonia"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh", "Nainital", "Almora"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri", "Asansol"]
    }
        
        self.setup_gui()
        
    def setup_gui(self):
        # Configure grid weight
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Heading
        heading_frame = tk.Frame(self.root)
        heading_frame.grid(row=0, column=0, pady=10, sticky="ew")
        
        # Back Button
        back_btn = tk.Button(heading_frame, text="← Back", command=self.go_back)
        back_btn.pack(side="left", padx=20)
        
        # Heading
        heading = tk.Label(heading_frame, text="Theater Search System", 
                         font=("Arial", 20, "bold"))
        heading.pack(side="left", expand=True)
        
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Left frame for search options
        left_frame = tk.Frame(main_frame, width=300)
        left_frame.grid(row=0, column=0, padx=(0, 20), sticky="n")
        
        # State Selection
        state_label = tk.Label(left_frame, text="Select State:")
        state_label.pack(pady=(0, 5), anchor="w")
        self.state_var = tk.StringVar()
        self.state_combo = ttk.Combobox(left_frame, textvariable=self.state_var, 
                                      values=self.states, width=25)
        self.state_combo.pack(pady=(0, 10), anchor="w")
        self.state_combo.bind("<<ComboboxSelected>>", self.update_cities)
        
        # City Selection
        city_label = tk.Label(left_frame, text="Select City:")
        city_label.pack(pady=(0, 5), anchor="w")
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(left_frame, textvariable=self.city_var, width=25)
        self.city_combo.pack(pady=(0, 10), anchor="w")
        
        # Locality Entry
        locality_label = tk.Label(left_frame, text="Enter Locality:")
        locality_label.pack(pady=(0, 5), anchor="w")
        self.locality_entry = tk.Entry(left_frame, width=27)
        self.locality_entry.pack(pady=(0, 10), anchor="w")
        
        # Search radius
        radius_label = tk.Label(left_frame, text="Search Radius (km):")
        radius_label.pack(pady=(0, 5), anchor="w")
        self.radius_var = tk.StringVar(value="5")
        self.radius_entry = tk.Entry(left_frame, textvariable=self.radius_var, width=27)
        self.radius_entry.pack(pady=(0, 10), anchor="w")
        
        # Proceed Button
        proceed_btn = tk.Button(left_frame, text="Search Theaters", 
                              command=self.search_theaters, width=20)
        proceed_btn.pack(pady=20)
        
        # Right frame for theater list
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        
        # Theater list label
        self.theater_label = tk.Label(right_frame, text="Available Theaters:", 
                                    font=("Arial", 12, "bold"))
        self.theater_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        # Create canvas and scrollbar for theater list
        self.canvas = tk.Canvas(right_frame)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", 
                                command=self.canvas.yview)
        self.theater_frame = tk.Frame(self.canvas)
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout for canvas and scrollbar
        self.canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        
        # Create window in canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.theater_frame, 
                                                    anchor="nw", tags="self.theater_frame")
        
        # Configure theater frame
        self.theater_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events for scrolling
        self.theater_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Variable for radio buttons
        self.selected_theater = tk.StringVar()

    def get_location_coordinates(self):
        state = self.state_var.get()
        city = self.city_var.get()
        locality = self.locality_entry.get()
        
        # Construct location string
        location = f"{locality}, {city}, {state}, India" if locality else f"{city}, {state}, India"
        
        try:
            lat, lon = get_lat_long_osm(location)
            if lat and lon:
                return float(lat), float(lon)
            else:
                messagebox.showerror("Error", "Location not found")
                return None, None
        except Exception as e:
            messagebox.showerror("Error", f"Error getting location: {str(e)}")
            return None, None

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Update the width of the canvas window when canvas is resized
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def search_theaters(self):
        self.clear_theaters()
        
        if not self.city_var.get():
            messagebox.showerror("Error", "Please select a city")
            return
        
        # Get coordinates for the selected location
        lat, lon = self.get_location_coordinates()
        if not lat or not lon:
            return
        
        try:
            radius = float(self.radius_var.get())
            theaters = self.theater_finder.get_nearby_theaters(lat, lon, radius)
            
            if not theaters:
                no_theaters_label = tk.Label(self.theater_frame, 
                                          text="No theaters found in the area",
                                          fg="red")
                no_theaters_label.grid(row=0, column=0, pady=10, sticky="w")
                return

            self.selected_theater = tk.StringVar(value=0)
            
            # Display theaters with distance
            for idx, theater in enumerate(theaters):
                frame = tk.Frame(self.theater_frame)
                frame.grid(row=idx, column=0, sticky="ew", pady=2)
                frame.grid_columnconfigure(0, weight=1)
                
                text = f"{theater['name']} ({theater['distance']} km)"
                rb = tk.Radiobutton(frame, text=text,
                                  variable=self.selected_theater,
                                  value=theater['name'],
                                  anchor="w")
                rb.grid(row=0, column=0, sticky="ew")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error searching theaters: {str(e)}")

    def go_back(self):
        response = messagebox.askyesno("Confirm", "Do you want to go back?")
        if response:
            self.root.quit()
            
    def update_cities(self, event=None):
        state = self.state_var.get()
        self.city_combo['values'] = self.cities.get(state, [])
        self.city_var.set("")  # Clear city selection
        self.clear_theaters()
        
    def clear_theaters(self):
        for widget in self.theater_frame.winfo_children():
            widget.destroy()

# ... [TheaterFinder class and other functions remain the same]
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

def get_lat_long_osm(location):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'MyGeocodingApp/1.0 (your-email@example.com)'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

if __name__ == "__main__":
    root = tk.Tk()
    app = TheaterSearchGUI(root)
    root.mainloop()
