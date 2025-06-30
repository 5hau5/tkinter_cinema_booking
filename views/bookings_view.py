import customtkinter as ctk
from controllers.booking_controller import BookingController  
from controllers.showtime_controller import ShowtimeController
from controllers.cinema_controller import CinemaController
from tkinter.messagebox import showerror, showinfo
import datetime

class BookingView(ctk.CTkFrame):
    def __init__(self, master, cinema_id, user_role):
        super().__init__(master)

        self.configure(fg_color='#282c33')
        self.rowconfigure((0,1), weight=0)
        self.rowconfigure((2), weight=1)
        self.columnconfigure(0, weight=1)


        self.cinema_id = cinema_id
        self.selected_cinema = cinema_id

        self.user_role = user_role

        self.controller = BookingController()
        self.cinema_controller = CinemaController()

        self.top_frame = ctk.CTkFrame(self, fg_color='#282c33')
        self.top_frame.columnconfigure((0,1,2), weight=1)
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=0, padx=0)

        # Filter Section
    
        self.date = None
        self.cinema_combo()

        # Date Filter
        self.search_frame = ctk.CTkFrame(master=self.top_frame, height=20, fg_color='#202329')
        self.search_frame.columnconfigure((0), weight=1)
        self.search_frame.grid(column=2, row=0, sticky='e', padx=5, pady=5)
        self.date_filter_entry = ctk.CTkEntry(self.search_frame, placeholder_text="YYYY-MM-DD")
        self.date_filter_entry.grid(row=0, column=0, padx=5, pady=5)

        # Filter and Clear Buttons
        filter_button = ctk.CTkButton(self.search_frame, text="Filter", command=self.apply_filters, width=40,)
        filter_button.grid(row=0, column=1, padx=5)

        clear_button = ctk.CTkButton(self.search_frame, text="Clear", command=self.clear_filters, width=40,)
        clear_button.grid(row=0, column=2, padx=5)

        # Scrollable Booking List
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color='#282c33')
        self.scrollable_frame.grid(row=2, column=0, sticky='nsew', padx=1, pady=1)

        
        self.headers = [
            "ID", "Booking REF", "Booked by", 
            "Film Title", "Screen", "Seats", 
            "Cost", "Date Booked", "Time", "Refund"
        ]
        self.header_row = ctk.CTkFrame(self, fg_color='#21252b')
        self.header_row.grid(row=1, column=0, sticky='ew', pady=2, padx=9)

        # Configure the grid columns with minsize and weight
        column_settings = [
            {"minsize": 40, "weight": 1},  # booking_id
            {"minsize": 142, "weight": 2}, # booking_ref (slightly increased space)
            {"minsize": 86, "weight": 2}, # username
            {"minsize": 173, "weight": 3}, # film_name
            {"minsize": 70, "weight": 1},  # screen_number
            {"minsize": 60, "weight": 1},  # booked_seats (reduced space)
            {"minsize": 70, "weight": 1},  # total_cost
            {"minsize": 110, "weight": 1}, # booking_date
            {"minsize": 100, "weight": 1},
            {"minsize": 70, "weight": 1},   # Refund column
        ]

        for i, settings in enumerate(column_settings):
            self.header_row.columnconfigure(i, minsize=settings["minsize"], weight=settings["weight"])

        # Add headers to the grid
        for i, header in enumerate(self.headers):
            label = ctk.CTkLabel(self.header_row, text=header, anchor="w")
            label.grid(row=0, column=i, sticky="w", padx=10, pady=2)


        # Load All Bookings Initially
        self.load_bookings()

    def cinema_combo(self):
        # Fetch cinemas and map names to IDs
        self.cinemas = self.cinema_controller.fetch_all_cinemas()
        self.cinema_name_to_id = {cinema[1]: cinema[0] for cinema in self.cinemas}

        # Cinema dropdown
        self.cinema_dropdown = ctk.CTkComboBox(
            self.top_frame,
            values=list(self.cinema_name_to_id.keys()),
            command=self.update_selected_cinema_id,
        )
        if self.user_role != 'staff':
            self.cinema_dropdown.grid(row=0, column=0, padx=10, sticky='ew')

        selected_cinema = self.cinema_controller.fetch_cinema_by_id(self.cinema_id)

        if selected_cinema:
            self.cinema_dropdown.set(selected_cinema[1])


    def update_selected_cinema_id(self, selected_cinema_name):
        self.selected_cinema = self.cinema_name_to_id.get(selected_cinema_name)
        self.load_bookings()

    def apply_filters(self):
        """
        Apply filters based on booking date.
        """
        try:
            # Get filter values
            booking_date = self.date_filter_entry.get().strip()
            self.date = booking_date
            self.load_bookings()
        except Exception as e:
            showerror("Error", f"An error occurred while applying filters: {str(e)}")

    def clear_filters(self):
        """
        Clear all filters and reload all bookings.
        """
        self.date_filter_entry.delete(0, "end")
        self.date = None
        self.load_bookings()

    def load_bookings(self):
        """
        Load and display all bookings.
        """
        self.clear_bookings()
        #try:
        bookings = self.controller.fetch_all_bookings(cinema_id=self.selected_cinema, date=self.date)

        for booking in bookings:
            row = BookRow(self.scrollable_frame, booking, self.refund_booking)
            row.pack(fill="x", pady=2, padx=2)

       # except Exception as e:
            #showerror("Error", f"An error occurred while loading bookings: {str(e)}")   

    def clear_bookings(self):
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def refund_booking(self, booking_detail):
        """
        Process the refund of a booking.
        """
        try:
            # Fetch showtime details
            showtime_details = ShowtimeController().fetch_showtime_by_id(int(booking_detail["booking_id"]))
            showtime_date = datetime.datetime.strptime(showtime_details[6], "%Y-%m-%d")  # Convert string to datetime object

            # Check if the showtime is at least 1 day (24 hours) away
            current_datetime = datetime.datetime.now()
            time_difference = (showtime_date - current_datetime).total_seconds()

            if time_difference > 86400:  # 86400 seconds = 1 day
                self.controller.cancel_booking(booking_detail["booking_id"])
                self.load_bookings()  # Refresh bookings list
                print(f"Booking {booking_detail['booking_id']} refunded successfully.")
            else:
                showerror("Refunds are only allowed at least 1 day before the showtime.") 
                print("Refunds are only allowed at least 1 day before the showtime.")

        except Exception as e:
            print(f"An error occurred while processing the refund: {str(e)}")


class BookRow(ctk.CTkFrame):
    def __init__(self, master, booking_details, refund_call):
        super().__init__(master)
        self.configure(fg_color='#333842')

        # Configure columns with a combination of minsize and weight
        column_settings = [
            {"minsize": 50, "weight": 1},  # booking_id
            {"minsize": 160, "weight": 2}, # booking_ref (slightly increased space)
            {"minsize": 100, "weight": 2}, # username
            {"minsize": 200, "weight": 3}, # film_name
            {"minsize": 80, "weight": 1},  # screen_number
            {"minsize": 70, "weight": 1},  # booked_seats (reduced space)
            {"minsize": 80, "weight": 1},  # total_cost
            {"minsize": 120, "weight": 1}, # booking_date
            {"minsize": 100, "weight": 1}, # booking_time
        ]

        for col, settings in enumerate(column_settings):
            self.columnconfigure(col, minsize=settings["minsize"], weight=settings["weight"])

        self.master = master
        self.booking_details = booking_details
        self.refund_call = refund_call

        # Display booking details
        keys = [
            "booking_id", "booking_ref", "username",
            "film_name", "screen_number", "booked_seats",
            "total_cost", "booking_date", "booking_time"
        ]

        for col, key in enumerate(keys):
            # Format specific fields
            value = booking_details[key]
            if key == "booked_seats":
                value = str(len(value.split(",")))  # Count the number of seats
            elif key == "total_cost":
                value = f"${float(value):.2f}"  # Format total cost as currency

            label = ctk.CTkLabel(
                self, text=str(value),
                anchor="w"  # Align text to the left
            )
            label.grid(row=0, column=col, sticky="w", padx=10)

        # Refund/Cancel button
        self.refund_button = ctk.CTkButton(self, text="REFUND", command=self.remove, width=80)
        self.refund_button.grid(row=0, column=len(keys), sticky="e", padx=10)


        # Fetch showtime details
        try:
            showtime_details = ShowtimeController().fetch_showtime_by_id(booking_details["showtime_id"])
            showtime_date = showtime_details[6]  # Assuming index 6 corresponds to the showtime date

            # Check if refund is allowed
            showtime_datetime = datetime.datetime.strptime(showtime_date, "%Y-%m-%d")
            current_datetime = datetime.datetime.now()
            time_difference = (showtime_datetime - current_datetime).total_seconds()

            if time_difference < 86400:  # Less than or equal to 1 day (24 hours)
                self.refund_button.configure(state="disabled")

        except Exception as e:
            print(f"Error fetching showtime details: {e}")
            self.refund_button.configure(state="disabled")

        #self.refund_button.grid(row=0, column=len(keys), sticky="e")

    def remove(self):
        """
        Trigger the refund process in the master view.
        """
        self.refund_call(self.booking_details)
        #self.master.master.refund_booking(self.booking_details)

