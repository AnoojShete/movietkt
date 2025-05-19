import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class MovieBookingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.root.geometry("800x500")
        
        # Create main container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create top frame for search and back button
        self.create_top_frame()
        
        # Create scrollable frame for movies
        self.create_scrollable_frame()
        
        # Load initial movies
        self.load_movies()

    def create_top_frame(self):
        # Top frame for search and back button
        top_frame = tk.Frame(self.main_container)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Back button
        back_button = ttk.Button(top_frame, text="Back", command=self.root.quit)
        back_button.pack(side=tk.LEFT, padx=5)
        
        # Search bar
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=50)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Search button
        search_button = ttk.Button(top_frame, text="Search", command=self.load_movies)
        search_button.pack(side=tk.LEFT, padx=5)

    def create_scrollable_frame(self):
        # Create a canvas with scrollbars
        self.canvas_frame = tk.Frame(self.main_container)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas
        self.canvas = tk.Canvas(self.canvas_frame)
        
        # Create vertical scrollbar
        v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure canvas
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create frame inside canvas for movie posters
        self.movie_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.movie_frame, anchor="nw")
        
        # Bind configure event to update scroll region
        self.movie_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind('<Configure>', self.frame_width)

    def frame_width(self, event):
        # Update the width to fit the canvas
        canvas_width = event.width
        self.canvas.itemconfig(1, width=canvas_width)

    def on_frame_configure(self, event=None):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def proceed_with_selection(self, movie_name):
        messagebox.showinfo("Selected Movie", f"You have selected {movie_name}!")

    def load_movies(self):
        # Clear existing movie posters
        for widget in self.movie_frame.winfo_children():
            widget.destroy()
            
        search_query = self.search_var.get().lower()
        movie_folder = "MoviePosters"  # Update this path to your movie posters folder
        
        # Counter for grid positioning
        row = 0
        col = 0
        max_columns = 4  # Number of movies per row
        
        try:
            for filename in os.listdir(movie_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    if search_query in filename.lower():
                        # Create frame for movie poster and details
                        poster_frame = tk.Frame(self.movie_frame, padx=10, pady=10)
                        poster_frame.grid(row=row, column=col, sticky='nsew')
                        
                        # Load and resize image
                        img_path = os.path.join(movie_folder, filename)
                        img = Image.open(img_path)
                        img = img.resize((150, 200), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        
                        # Create and pack image label
                        img_label = tk.Label(poster_frame, image=photo)
                        img_label.image = photo
                        img_label.pack()
                        
                        # Movie title
                        movie_name = filename[:-4]  # Remove file extension
                        title_label = tk.Label(poster_frame, text=movie_name, wraplength=150)
                        title_label.pack(pady=(5, 0))
                        
                        # Book button
                        book_button = ttk.Button(poster_frame, text="Book Now",
                                              command=lambda m=movie_name: self.proceed_with_selection(m))
                        book_button.pack(pady=5)
                        
                        # Update grid position
                        col += 1
                        if col >= max_columns:
                            col = 0
                            row += 1
        
        except FileNotFoundError:
            messagebox.showerror("Error", f"Movie poster directory '{movie_folder}' not found!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieBookingDashboard(root)
    root.mainloop()
