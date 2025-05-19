import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

class DateSelectionApp:
    def __init__(self, master):
        self.master = master
        master.title("Select a Date")

        # Create a label
        self.label = tk.Label(master, text="Choose a date for your movie:")
        self.label.pack(pady=10)

        # Create a calendar widget
        self.calendar = Calendar(master, selectmode='day', year=2024, month=10, day=29)
        self.calendar.pack(pady=20)

        # Create a submit button
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_date)
        self.submit_button.pack(pady=10)

    def submit_date(self):
        selected_date = self.calendar.get_date()
        messagebox.showinfo("Selected Date", f"You selected: {selected_date}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DateSelectionApp(root)
    root.mainloop()
