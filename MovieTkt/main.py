import mysql.connector as sqltor
#import moviedetails

def connectDatabase(host="localhost", user="root", password="Anooj@23", db="Movietkt"):	
	try:
		global mydb
		mydb = sqltor.connect(
			host = host,
			user = user,
			password = password,
			database = db
			)

		if mydb.is_connected():
			print("Connected to MySQL database successfully.")

	except Exception as e:
		print(f"Something went wrong! {e}")


def createCustomer(fname, lname, email, phone):
	query = "INSERT INTO Customers(first_name, last_name, email, phone) values(%s, %s, %s, %s)"
	values = (fname, lname, email, phone)
	try:
		cursor = mydb.cursor()
		cursor.execute(query, values)
		mydb.commit()
		print("Customer added successfully.")
	except Exception as e:
		print(f"Something went wrong while inserting into customers! {e}")


def createMovie(title, genre, duration, director, release_date, rating, description, poster):
	query = "INSERT INTO Movies(title, genre, duration, director, release_date, rating, description, poster_url) values(%s, %s, %s, %s, %s, %s, %s, %s)"
	values = (title, genre, duration, director, release_date, rating, description, poster)
	try:
		cursor = mydb.cursor()
		cursor.execute(query, values)
		mydb.commit()
		print("Movie added successfully.")
	except Exception as e:
		print(f"Something went wrong while inserting into movies! {e}")

def createPayment(booking_id, amount, payment_method):
	query = "INSERT INTO Payments(booking_id, amount, payment_method) values(%s, %s, %s)"
	values = (booking_id, amount, payment_method)
	try:
		cursor = mydb.cursor()
		cursor.execute(query, values)
		mydb.commit()
		print("Payment made successfully.")
	except Exception as e:
		print(f"Something went wrong while inserting into Payments! {e}")

def createBooking(customer_id, showtime_id, number_of_tickets):
	query = "INSERT INTO Bookings(customer_id, showtime_id, number_of_tickets) values(%s, %s, %s)"
	values = (customer_id, showtime_id, number_of_tickets)
	try:
		cursor = mydb.cursor()
		cursor.execute(query, values)
		mydb.commit()
		print("Booking done successfully.")
	except Exception as e:
		print(f"Something went wrong while inserting into Bookings! {e}")

def createReview(movie_id, customer_id, rating, comment):
	query = "INSERT INTO Reviews(movie_id, customer_id, rating, comment) values(%s, %s, %s, %s)"
	values = (movie_id, customer_id, rating, comment)
	try:
		cursor = mydb.cursor()
		cursor.execute(query, values)
		mydb.commit()
		print("Review made successfully.")
	except Exception as e:
		print(f"Something went wrong while inserting into Reviews! {e}")

def createShowtime(movie_id, theater_id, show_date, show_time, available_seats):
	query = "INSERT INTO Showtimes(movie_id, theater_id, show_date, show_time, available_seats) values(%s, %s, %s, %s, %s)"
	values = (movie_id, theater_id, show_date, show_time, available_seats)
	try:
		cursor = mydb.cursor()
		cursor.execute(query, values)
		mydb.commit()
		print("Showtime created successfully.")
	except Exception as e:
		print(f"Something went wrong while inserting into Showtimes! {e}")

def createTheater(theater_name, location, total_seats):
	query = "INSERT INTO Theaters(theater_name, location, total_seats) values(%s, %s, %s)"
	values = (theater_name, location, total_seats)
	try:
		cursor = mydb.cursor()
		cursor.execute(query, values)
		mydb.commit()
		print("Theater created successfully.")
	except Exception as e:
		print(f"Something went wrong while inserting into Theaters! {e}")


'''
connectDatabase()
# createCustomer("Anooj", "Shete", "anooj@gmail.com", 7385776309)
movie_name = input("Enter a movie name: ")
import moviedetails
movie_info = moviedetails.getMovie(movie_name)
createMovie(movie_info['title'], movie_info['genre'], movie_info['duration'], movie_info['director'], movie_info['releasedate'], movie_info['rating'], movie_info['description'], movie_info['poster'])
'''
