import tkinter as tk
from tkinter import messagebox

class TheaterBookingApp:
    def __init__(self, master):
        self.master = master
        master.title("Theater Booking System")

        # Theater name
        self.theater_name = "Awesome Theater"
        self.label = tk.Label(master, text=self.theater_name, font=("Helvetica", 16))
        self.label.grid(row=0, columnspan=5, pady=10)  # Use grid here

        # Create a grid of seats
        self.seats = []
        self.rows = 10  # Number of rows
        self.cols = 10  # Number of columns
        for i in range(self.rows):
            row_seats = []
            for j in range(self.cols):
                seat_button = tk.Button(master, text=f"Seat {i * self.cols + j + 1}", width=10,
                                        command=lambda i=i, j=j: self.toggle_seat(i, j))
                seat_button.grid(row=i+1, column=j, padx=5, pady=5)  # Use grid here
                row_seats.append({"button": seat_button, "booked": False})
            self.seats.append(row_seats)

        # Proceed to pay button
        self.pay_button = tk.Button(master, text="Proceed to Pay", command=self.proceed_to_pay)
        self.pay_button.grid(row=self.rows + 1, columnspan=self.cols, pady=20)  # Use grid here

    def toggle_seat(self, row, col):
        """Toggle seat booking status."""
        seat = self.seats[row][col]
        if seat["booked"]:
            seat["booked"] = False
            seat["button"].config(bg="SystemButtonFace")  # Reset color
        else:
            seat["booked"] = True
            seat["button"].config(bg="grey")  # Mark as booked

    def proceed_to_pay(self):
        """Handle payment process."""
        booked_seats = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.seats[i][j]["booked"]:
                    booked_seats.append(f"Seat {i * self.cols + j + 1}")
        
        if booked_seats:
            messagebox.showinfo("Booking Confirmed", f"You have booked: {', '.join(booked_seats)}")
        else:
            messagebox.showwarning("No Seats Selected", "Please select at least one seat to proceed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TheaterBookingApp(root)
    root.mainloop()
