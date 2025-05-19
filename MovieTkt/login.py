import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import hashlib
import re

class MovieTicketLogin:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("FlickNation - The Ultimate Movie Ticket Booking System")
        self.window.geometry("800x500")
        self.window.resizable(False, False)
        
        # Configure color scheme
        self.primary_color = "#2c3e50"  # Dark blue
        self.secondary_color = "#3498db"  # Light blue
        self.bg_color = "#ecf0f1"  # Light gray
        self.text_color = "#2c3e50"  # Dark blue
        
        # Configure window
        self.window.configure(bg=self.bg_color)
        
        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Anooj@23",
            database="Movietkt"
        )
        self.cursor = self.db.cursor()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="FlickNation - Movie Ticket Booking System",
            font=("Arial", 24, "bold"),
            fg=self.primary_color,
            bg=self.bg_color
        )
        title_label.pack(pady=2)
        
        quote_label = tk.Label(
            main_frame,
            text="Entertainment made easy.",
            font=("Helvetica 12 italic"),
            fg=self.primary_color,
            bg=self.bg_color
        )
        quote_label.pack()
        
        # Login frame
        login_frame = tk.Frame(main_frame, bg=self.bg_color)
        login_frame.pack(pady=20)
        
        # Username
        username_frame = tk.Frame(login_frame, bg=self.bg_color)
        username_frame.pack(pady=10)
        
        username_label = tk.Label(
            username_frame,
            text="Username:",
            font=("Helvetica", 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        username_label.pack(side=tk.LEFT, padx=10)
        
        self.username_entry = ttk.Entry(
            username_frame,
            font=("Helvetica", 12),
            width=30
        )
        self.username_entry.pack(side=tk.LEFT)
        
        # Password
        password_frame = tk.Frame(login_frame, bg=self.bg_color)
        password_frame.pack(pady=10)
        
        password_label = tk.Label(
            password_frame,
            text="Password:",
            font=("Helvetica", 12),
            fg=self.text_color,
            bg=self.bg_color
        )
        password_label.pack(side=tk.LEFT, padx=10)
        
        self.password_entry = ttk.Entry(
            password_frame,
            font=("Helvetica", 12),
            width=30,
            show="•"
        )
        self.password_entry.pack(side=tk.LEFT)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        # Login button
        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            font=("Helvetica", 12),
            padding=10
        )
        
        login_button = ttk.Button(
            button_frame,
            text="Login",
            style="Custom.TButton",
            command=self.login
        )
        login_button.pack(side=tk.LEFT, padx=10)
        
        # Register button
        register_button = ttk.Button(
            button_frame,
            text="Register",
            style="Custom.TButton",
            command=self.show_register
        )
        register_button.pack(side=tk.LEFT, padx=10)
        
        # Forgot password link
        forgot_password = tk.Label(
            main_frame,
            text="Forgot Password?",
            font=("Helvetica", 10, "underline"),
            fg=self.secondary_color,
            bg=self.bg_color,
            cursor="hand2"
        )
        forgot_password.pack(pady=10)
        forgot_password.bind("<Button-1>", self.forgot_password)

    def create_registration_form(self, register_window):
        # Main frame for registration
        main_frame = tk.Frame(register_window, bg=self.bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Create New Account",
            font=("Helvetica", 24, "bold"),
            fg=self.primary_color,
            bg=self.bg_color
        )
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(main_frame, bg=self.bg_color)
        form_frame.pack(pady=20)
        
        # Create labels and entries for each field
        fields = [
            ("Full Name:", "name_entry"),
            ("Email:", "email_entry"),
            ("Phone:", "phone_entry"),
            ("Username:", "reg_username_entry"),
            ("Password:", "reg_password_entry"),
            ("Confirm Password:", "confirm_password_entry")
        ]
        
        self.reg_entries = {}  # Store entries for later access
        
        for label_text, entry_name in fields:
            frame = tk.Frame(form_frame, bg=self.bg_color)
            frame.pack(pady=10)
            
            label = tk.Label(
                frame,
                text=label_text,
                font=("Helvetica", 12),
                fg=self.text_color,
                bg=self.bg_color,
                width=15,
                anchor="e"
            )
            label.pack(side=tk.LEFT, padx=10)
            
            # Create entry with password masking if it's a password field
            show_char = "•" if "password" in entry_name.lower() else ""
            entry = ttk.Entry(
                frame,
                font=("Helvetica", 12),
                width=30,
                show=show_char
            )
            entry.pack(side=tk.LEFT)
            
            self.reg_entries[entry_name] = entry
        
        # Register button
        register_button = ttk.Button(
            main_frame,
            text="Register",
            style="Custom.TButton",
            command=lambda: self.register_user(register_window)
        )
        register_button.pack(pady=20)

    def validate_registration(self):
        # Get all values
        name = self.reg_entries["name_entry"].get()
        email = self.reg_entries["email_entry"].get()
        phone = self.reg_entries["phone_entry"].get()
        username = self.reg_entries["reg_username_entry"].get()
        password = self.reg_entries["reg_password_entry"].get()
        confirm_password = self.reg_entries["confirm_password_entry"].get()
        
        # Validate each field
        if not all([name, email, phone, username, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required!")
            return False
            
        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Invalid email format!")
            return False
            
        # Phone validation
        phone_pattern = r'^\d{10}$'
        if not re.match(phone_pattern, phone):
            messagebox.showerror("Error", "Phone number must be 10 digits!")
            return False
            
        # Password validation
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters!")
            return False
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return False
            
        return True

    def register_user(self, register_window):
        if not self.validate_registration():
            return
            
        try:
            # Insert into customer table
            self.cursor.execute("""
                INSERT INTO customer (name, email, phone)
                VALUES (%s, %s, %s)
            """, (
                self.reg_entries["name_entry"].get(),
                self.reg_entries["email_entry"].get(),
                self.reg_entries["phone_entry"].get()
            ))
            
            customer_id = self.cursor.lastrowid
            
            # Insert into customer_auth table
            self.cursor.execute("""
                INSERT INTO customer_auth (customer_id, username, password_hash)
                VALUES (%s, %s, %s)
            """, (
                customer_id,
                self.reg_entries["reg_username_entry"].get(),
                hashlib.sha256(self.reg_entries["reg_password_entry"].get().encode()).hexdigest()
            ))
            
            self.db.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            register_window.destroy()
            self.window.deiconify()
            
        except mysql.connector.Error as err:
            self.db.rollback()
            if "Duplicate entry" in str(err):
                if "username" in str(err):
                    messagebox.showerror("Error", "Username already exists!")
                elif "email" in str(err):
                    messagebox.showerror("Error", "Email already registered!")
            else:
                messagebox.showerror("Error", f"Database error: {err}")
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            # Check credentials
            self.cursor.execute("""
                SELECT * FROM customer_auth 
                WHERE username = %s AND password_hash = %s
            """, (username, hashed_password))
            
            user = self.cursor.fetchone()
            
            if user:
                messagebox.showinfo("Success", "Login successful!")
                self.window.destroy()
                # Here you would typically open the main booking window
                # self.open_booking_window()
            else:
                messagebox.showerror("Error", "Invalid username or password")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
    
    def show_register(self):
        # Hide login window
        self.window.withdraw()
        
        # Create registration window
        register_window = tk.Toplevel()
        register_window.title("Register")
        register_window.geometry("800x600")
        register_window.configure(bg=self.bg_color)
        
        # Create registration form
        self.create_registration_form(register_window)
        
        # Handle window closing
        register_window.protocol("WM_DELETE_WINDOW", 
            lambda: (register_window.destroy(), self.window.deiconify()))
    
    def forgot_password(self, event):
        # Implement password recovery functionality
        messagebox.showinfo("Reset Password", 
            "Password reset link will be sent to your registered email.")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = MovieTicketLogin()
    app.run()
