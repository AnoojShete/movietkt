import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

root = tk.Tk()
root.title("Payment System - Movie Ticket Booking")
root.geometry("800x500")

# Initialize variables
ticket_price = 200  # Default price
num_tickets = 1      # Default number of tickets
total_amount = ticket_price * num_tickets

# Payment details
card_number = tk.StringVar()
card_holder = tk.StringVar()
expiry_month = tk.StringVar()
expiry_year = tk.StringVar()
cvv = tk.StringVar()

def create_payment_page():
    # Title
    title_frame = tk.Frame(root)
    title_frame.pack(pady=20)
    
    title = tk.Label(title_frame, text="Payment Details", font=("Arial", 20, "bold"))
    title.pack()

    # Booking Summary
    summary_frame = tk.LabelFrame(root, text="Booking Summary", padx=20, pady=10)
    summary_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(summary_frame, text=f"Number of Tickets: {num_tickets}").pack()
    tk.Label(summary_frame, text=f"Price per Ticket: ₹{ticket_price}").pack()
    tk.Label(summary_frame, text=f"Total Amount: ₹{total_amount}", 
            font=("Arial", 12, "bold")).pack()

    # Payment Method
    payment_frame = tk.LabelFrame(root, text="Payment Method", padx=20, pady=10)
    payment_frame.pack(pady=10, padx=20, fill="x")

    # Card Number
    tk.Label(payment_frame, text="Card Number:").pack(anchor="w")
    card_entry = tk.Entry(payment_frame, textvariable=card_number)
    card_entry.pack(fill="x", pady=5)

    # Card Holder Name
    tk.Label(payment_frame, text="Card Holder Name:").pack(anchor="w")
    holder_entry = tk.Entry(payment_frame, textvariable=card_holder)
    holder_entry.pack(fill="x", pady=5)

    # Expiry Date
    expiry_frame = tk.Frame(payment_frame)
    expiry_frame.pack(fill="x", pady=5)

    tk.Label(expiry_frame, text="Expiry Date:").pack(side="left")
    
    month_cb = ttk.Combobox(expiry_frame, textvariable=expiry_month, width=3)
    month_cb['values'] = [str(i).zfill(2) for i in range(1, 13)]
    month_cb.pack(side="left", padx=5)

    tk.Label(expiry_frame, text="/").pack(side="left")

    year_cb = ttk.Combobox(expiry_frame, textvariable=expiry_year, width=5)
    current_year = datetime.now().year
    year_cb['values'] = [str(i) for i in range(current_year, current_year + 11)]
    year_cb.pack(side="left", padx=5)

    # CVV
    tk.Label(payment_frame, text="CVV:").pack(anchor="w")
    cvv_entry = tk.Entry(payment_frame, textvariable=cvv, show="*", width=5)
    cvv_entry.pack(pady=5)

create_payment_page()
