import customtkinter as ctk
from views.film_view import FilmFrame
from controllers.booking_controller import BookingController
from controllers.showtime_controller import ShowtimeController
from controllers.cinema_controller import CinemaController
import datetime
import textwrap

class BookView(ctk.CTkFrame):
    def __init__(self, master, film_id, showtimes, user_id, cinema_id):
        super().__init__(master)
        self.configure(fg_color='#282c33')
        self.rowconfigure((0,1,2,3), weight=0)
        self.columnconfigure((0,1,2,3), weight=1)

        self.film_id = film_id
        self.showtimes = showtimes
        self.user_id = user_id
        self.cinema_id =  cinema_id

        self.master = master

        self.booking_controller = BookingController()
        self.showtime_controller = ShowtimeController()
        self.cinema_controller = CinemaController()

        self.selected_showtime_id = None
        self.selected_showtime_price = None
        self.selected_seats = None

        self.film_frame = FilmFrame(master=self, film_id=self.film_id)
        self.film_frame.grid(row=0, columnspan=4, pady=5, padx=5)

        self.seat_entry = ctk.CTkEntry(master=self)
        self.select_seat_button = ctk.CTkButton(master=self, command=self.select_seats, text="SELECT")
        self.total_price_label = ctk.CTkLabel(master=self)

        self.available_seats = None  # Holds the available seats for the selected showtime

        # Create a dropdown to select a showtime
        self.showtime_dropdown = ctk.CTkComboBox(
            self,
            values=["Select a Showtime"] + [self.showtime_controller.fetch_showtime_by_id(showtime_id=showtime_id)[7] for showtime_id in self.showtimes],
            command=self.update_seats
        )
        self.showtime_dropdown.grid(row=1, column=3, padx=5, pady=5, sticky="ew") 

        # Label to display available seats
        self.seats_label = ctk.CTkLabel(self, text="Available Seats: Select a Showtime", fg_color='#202329')
        self.seats_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.vip_seats_label = ctk.CTkLabel(self, text="Vip Seats:", fg_color='#202329')
        self.vip_seats_label.grid(row=2, column=0, columnspan=1, rowspan=2, padx=5, pady=5, sticky="nsew")

        self.upper_seats_label = ctk.CTkLabel(self, text="Upper Hall Seats:", fg_color='#202329')
        self.upper_seats_label.grid(row=2, column=1, columnspan=1, rowspan=2, padx=5, pady=5, sticky="nsew")

        self.lower_seats_label = ctk.CTkLabel(self, text="Vip Seats:", fg_color='#202329')
        self.lower_seats_label.grid(row=2, column=2, columnspan=1, rowspan=2, padx=5, pady=5, sticky="nsew")

        self.make_booking_button = ctk.CTkButton(master=self, text='BOOK', command=self.make_booking, state="disabled")
        self.make_booking_button.grid(row=4, column=3, pady=10, padx=10)

    def update_seats(self, selected_showtime_time):
        """
        Fetches the available seats for the selected showtime and updates the seat labels.
        """
        # Find the showtime_id corresponding to the selected time
        for showtime_id in self.showtimes:
            showtime_time = self.showtime_controller.fetch_showtime_by_id(showtime_id=showtime_id)[7]
            if showtime_time == selected_showtime_time:
                self.selected_showtime_id = showtime_id
                self.selected_showtime_price = self.showtime_controller.fetch_showtime_by_id(showtime_id=self.selected_showtime_id)[8]
                break
        else:
            # No valid selection made
            self.seats_label.configure(text="Invalid Showtime Selected")
            return

        # Fetch available seats for the selected showtime
        self.available_seats = self.booking_controller.fetch_available_seats(self.selected_showtime_id)
        print(f"Available seats: {self.available_seats}")

        # Format the seat data for display
        if self.available_seats:
            # VIP Seats
            vip_seats = self.available_seats['vip']
            vip_seats_text = f"VIP Seats ({len(vip_seats)}):\n" + "\n".join(textwrap.wrap(", ".join(map(str, vip_seats)), width=20))
            self.vip_seats_label.configure(text=vip_seats_text)

            # Upper Hall Seats
            upper_hall_seats = self.available_seats['upper_hall']
            upper_hall_seats_text = f"Upper Hall Seats ({len(upper_hall_seats)}):\n" + "\n".join(textwrap.wrap(", ".join(map(str, upper_hall_seats)), width=20))
            self.upper_seats_label.configure(text=upper_hall_seats_text)

            # Lower Hall Seats
            lower_hall_seats = self.available_seats['lower_hall']
            lower_hall_seats_text = f"Lower Hall Seats ({len(lower_hall_seats)}):\n" + "\n".join(textwrap.wrap(", ".join(map(str, lower_hall_seats)), width=20))
            self.lower_seats_label.configure(text=lower_hall_seats_text)

            # Enable the seat selection controls
            self.seat_entry.grid(row=2, column=3, sticky='ew', pady=10, padx=10)
            self.select_seat_button.grid(row=3, column=3, pady=10, padx=10)
        else:
            # No seats available
            self.seats_label.configure(text="No Seats Available for the Selected Showtime")
            self.vip_seats_label.configure(text="VIP Seats: None")
            self.upper_seats_label.configure(text="Upper Hall Seats: None")
            self.lower_seats_label.configure(text="Lower Hall Seats: None")

    def select_seats(self):
        """
        - Check if the seats in the entry box are valid.
        - Ensure no seat is selected more than once.
        - Count how many seats are VIP, Upper Hall, and Lower Hall.
        - Calculate the total price for the selected seats using the formula:
            (1.44v + 1.2u + l) * p
            where: 
                v = number of VIP seats,
                u = number of Upper Hall seats,
                l = number of Lower Hall seats,
                p = self.selected_showtime_price.
        """
        # Get the selected seats from the entry box
        selected_seats_input = self.seat_entry.get()

        try:
            # Parse the input as a list of integers
            selected_seats = list(map(int, selected_seats_input.replace(" ", "").split(',')))
        except ValueError:
            self.total_price_label.configure(text="Invalid seat numbers entered")
            self.make_booking_button.configure(state="disabled")
            return

        # Check for duplicate seat numbers
        if len(selected_seats) != len(set(selected_seats)):
            self.total_price_label.configure(text="Duplicate seat numbers entered")
            self.make_booking_button.configure(state="disabled")
            return

        # Validate that all selected seats are available
        invalid_seats = [seat for seat in selected_seats if
                        seat not in self.available_seats['vip'] and
                        seat not in self.available_seats['upper_hall'] and
                        seat not in self.available_seats['lower_hall']]

        if invalid_seats:
            self.total_price_label.configure(text=f"Invalid Seats: {', '.join(map(str, invalid_seats))}")
            self.make_booking_button.configure(state="disabled")
            return

        # Count the number of seats in each section
        num_vip = sum(1 for seat in selected_seats if seat in self.available_seats['vip'])
        num_upper_hall = sum(1 for seat in selected_seats if seat in self.available_seats['upper_hall'])
        num_lower_hall = sum(1 for seat in selected_seats if seat in self.available_seats['lower_hall'])

        # Calculate the total price
        if self.selected_showtime_price is None:
            self.total_price_label.configure(text="Showtime price not set")
            self.make_booking_button.configure(state="disabled")
            return

        self.total_price = (1.44 * num_vip + 1.2 * num_upper_hall + num_lower_hall) * self.selected_showtime_price

        # Update the total price label
        self.total_price_label.configure(text=f"Total Price: ${self.total_price:.2f}")
        self.total_price_label.grid(row=3, column=1, sticky='ew')

        # Enable the booking button
        self.make_booking_button.configure(state="normal")

        # Disable booking button if the seat entry box is edited
        def disable_booking_on_edit(event):
            self.make_booking_button.configure(state="disabled")

        self.seat_entry.bind("<KeyRelease>", disable_booking_on_edit)

    def make_booking(self):
        self.make_booking_button.configure(state="disabled")
        current_datetime = datetime.datetime.now()
        date = current_datetime.strftime("%Y-%m-%d")
        time = current_datetime.strftime("%H:%M")

        seats = ', '.join(seat.strip() for seat in self.seat_entry.get().split(','))
        self.booking_ref = f"RF{datetime.datetime.now().strftime('%Y%m%d')}{f'{self.cinema_id:02}'}{f'{self.selected_showtime_id:04}'}{f'{(self.booking_controller.count_bookings(self.selected_showtime_id)+1):03}'}"


        self.booking_controller.create_booking(
            booking_ref=self.booking_ref,
            user_id=self.user_id, 
            showtime_id=self.selected_showtime_id, 
            seats=seats, 
            total_cost=self.total_price,
            date=date,
            time=time,
            cinema_id = self.cinema_id
        )
        self.make_reciept()

        self.master.back()

    def make_reciept(self):
        try:
            showtime = self.showtime_controller.fetch_showtime_by_id(self.selected_showtime_id)
            
            # Format receipt details
            num_tickets = len(self.seat_entry.get().split(','))
            receipt_content = f"""
            Booking Receipt
            ----------------------
            Booking Reference: {self.booking_ref}
            Film Name: {showtime[1]}
            Showtime Date: {showtime[6]}
            Showtime Time: {showtime[7]}
            Screen #: {showtime[3].split()[-1]}
            Number of Tickets: {num_tickets}
            Seat Numbers: {self.seat_entry.get()}
            Total Booking Cost: ${self.total_price:.2f}
            Booking Date: {datetime.datetime.now().strftime('%Y-%m-%d')}
            ----------------------
            Thank you for booking with us!
            """

            # Save receipt to a file
            file_name = f"receipt_{self.booking_ref}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            with open(file_name, "w") as receipt_file:
                receipt_file.write(receipt_content)

            print(f"Receipt saved as {file_name}")

        except Exception as e:
            print(f"Error generating receipt: {e}")