import sqlite3
from datetime import datetime
from models.booking_model import BookingModel

class BookingController:
    """
    Controller to manage booking operations.
    """

    def __init__(self):
        # Dictionary to store bookings
        # Example structure: {booking_id: {"user": ..., "film": ..., "date": ..., "time": ..., "seats": ...}}
        self.model = BookingModel()
        self.bookings = {}
        self.booking_id_counter = 1  # To generate unique booking IDs

    def create_booking(self, booking_ref, user_id, showtime_id, seats, total_cost, date, time, cinema_id):
        self.model.create_booking(booking_ref,user_id,showtime_id,seats,total_cost,date,time, cinema_id)

    def count_bookings(self, showtime_id):
        return self.model.count_bookings(showtime_id=showtime_id)

    def get_booking(self, booking_id):
        """
        Retrieve details of a specific booking.
        :param booking_id: The booking ID.
        :return: Booking details or None if not found.
        """
        return self.bookings.get(booking_id, None)

    def cancel_booking(self, booking_id):
        self.model.cancel_booking(booking_id)

    def fetch_all_bookings(self, cinema_id, date=None):
        return self.model.get_all_bookings(cinema_id, date)
    
    def fetch_all_bookings_by_user_id(self, user_id, month):
        return self.model.get_all_bookings_by_user_id(user_id, month)
    
    def fetch_all_bookings_by_film_id(self, film_id):
        return self.model.get_all_bookings_by_film_id(film_id)
    
    def fetch_all_bookings_by_showtime_id(self, showtime_id):
        return self.model.get_all_bookings_by_showtime_id(showtime_id)
        
    def fetch_available_seats(self, showtime):
        return self.model.get_all_available_seats(showtime)
    
