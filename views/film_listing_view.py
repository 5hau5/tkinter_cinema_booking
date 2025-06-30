import customtkinter as ctk
from controllers.film_listing_controller import FilmListingController
from controllers.cinema_controller import CinemaController
from views.film_view import FilmFrame
from views.book_view import BookView
import datetime

class FilmListingView(ctk.CTkFrame):
    def __init__(self, master, user_role, cinema_id, user_id):
        super().__init__(master)
        self.film_controller = FilmListingController()
        self.cinema_controller = CinemaController()

        self.configure(fg_color='#282c33')
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 3), weight=0)
        self.rowconfigure(2, weight=1)

        self.user_role = user_role
        self.user_id = user_id
        self.cinema_id = cinema_id
        self.selected_cinema = cinema_id
        self.current_datetime = datetime.datetime.now()
        
        print(self.current_datetime)

        
        # Search
        self.search_frame = ctk.CTkFrame(master=self, height=20, fg_color='#202329')
        self.search_frame.columnconfigure((0), weight=1)
        self.filmls_search_bar = ctk.CTkEntry(master=self.search_frame)
        self.search_text = self.filmls_search_bar.get()
        self.button_search_filmls = ctk.CTkButton(
            master=self.search_frame,
            text="Search",
            command=self.update_search_text,
            width=40,
        )

        self.cinema_combo()

        # Navigation buttons
        self.page_nav_frame = ctk.CTkFrame(master=self, fg_color='#202329')
        self.page_nav_frame.columnconfigure((0,1,2), weight=1)
        self.date_label = ctk.CTkLabel(master=self.page_nav_frame, text=self.current_datetime.strftime('%Y-%m-%d'))
        self.next_page_button = ctk.CTkButton(master=self.page_nav_frame, text='Next Day', command=self.page_next)
        self.prev_page_button = ctk.CTkButton(master=self.page_nav_frame, text='Previous Day', command=self.page_prev, state="disabled")

        # Film listings scroll frame
        self.filmls_scroll_frame = ctk.CTkScrollableFrame(
            master=self,
            fg_color='#282c33',
            border_width=2,
            border_color='#202329',
            corner_radius=0,
        )
        self.filmls_scroll_frame.rowconfigure((0, 1, 2), weight=1)
        self.filmls_scroll_frame.columnconfigure((0), weight=0)

        self.place_elements()
        self.load_filmls()

    def cinema_combo(self):
        # Fetch cinemas and map names to IDs
        self.cinemas = self.cinema_controller.fetch_all_cinemas()
        self.cinema_name_to_id = {cinema[1]: cinema[0] for cinema in self.cinemas}

        # Cinema dropdown
        self.cinema_dropdown = ctk.CTkComboBox(
            self,
            values=list(self.cinema_name_to_id.keys()),
            command=self.update_selected_cinema_id,
        )
        selected_cinema = self.cinema_controller.fetch_cinema_by_id(self.cinema_id)

        if selected_cinema:
            self.cinema_dropdown.set(selected_cinema[1])

    def place_elements(self):
        self.search_frame.grid(column=2, row=1, sticky='ew', padx=5, pady=5)

        self.filmls_search_bar.grid(column=0, row=0, sticky='ew', padx=5, pady=5)
        self.button_search_filmls.grid(column=1, row=0, sticky='e', padx=5, pady=5)

        if self.user_role != "staff":
            self.cinema_dropdown.grid(column=0, row=1, sticky='ew', padx=5, pady=5)

        self.page_nav_frame.grid(column=1, row=1, sticky='ew', padx=5, pady=5)

        self.date_label.grid(row=0, column=1, padx=5, pady=5)
        self.next_page_button.grid(row=0, column=2, sticky='e', padx=5, pady=5)
        self.prev_page_button.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.filmls_scroll_frame.grid(column=0, row=2, columnspan=5, rowspan=1, sticky='nsew', padx=2, pady=2)


    def update_selected_cinema_id(self, selected_cinema_name):
        self.selected_cinema = self.cinema_name_to_id.get(selected_cinema_name)
        self.load_filmls()

    def load_filmls(self):
        self.forget_filmls()
        print(f"Loading films for cinema ID: {self.selected_cinema}, datetime: {self.current_datetime}")

        self.film_listings = self.film_controller.fetch_all_film_listings(
            cinema_id=self.selected_cinema,
            datetime=self.current_datetime
        )

        print(self.film_listings)

        for film_id, showtime_list in self.film_listings.items():
            FilmListingFrame(master=self.filmls_scroll_frame, booking_function=self.make_booking, film_id=film_id, showtime_list=showtime_list).pack(fill="x", pady=2, padx=2)
        # Populate the scrollable frame with film listings

    def update_search_text(self):
        # strip sanitize the input
        self.search_text = self.filmls_search_bar.get().strip()

        # validate input (optional, but useful to restrict allowed characters)
        import re
        if not re.match(r'^[a-zA-Z0-9\s]*$', self.search_text):  # Alphanumeric and spaces only
            print("Invalid search text entered!")
            self.search_text = ""  # Reset invalid input

        self.load_filmls()

    def page_next(self):
        self.prev_page_button.configure(state="normal")
        self.current_datetime += datetime.timedelta(days=1)
        self.current_datetime = self.current_datetime.replace(hour=0, minute=0)
        self.date_label.configure(text=self.current_datetime.strftime('%Y-%m-%d'))
        self.load_filmls()

    def page_prev(self):
        if self.current_datetime.date() > datetime.datetime.now().date():
            self.current_datetime -= datetime.timedelta(days=1)
            self.current_datetime = self.current_datetime.replace(hour=0, minute=0)
            self.date_label.configure(text=self.current_datetime.strftime('%Y-%m-%d'))
            if self.current_datetime.date() == datetime.datetime.now().date():
                self.prev_page_button.configure(state="disabled")
            self.load_filmls()

            

    def forget_filmls(self):
        for widget in self.filmls_scroll_frame.winfo_children():
            widget.destroy()

    def make_booking(self, film_id, showtimes):
        self.forget_filmls()
        self.book_view = BookView(master=self, film_id=film_id, showtimes=showtimes, user_id=self.user_id, cinema_id=self.selected_cinema)
        self.book_view.grid(row=0, column=0, rowspan=4, columnspan=5, sticky='nsew')

    def back(self):
        self.book_view.destroy()
        self.load_filmls()
      

class FilmListingFrame(ctk.CTkFrame):
    def __init__(self, master, booking_function, film_id, showtime_list):
        super().__init__(master)

        self.configure(fg_color='#282c33')
        self.film_id = film_id
        self.columnconfigure((0,1), weight=0)

        self.booking_function = booking_function

        self.film = FilmFrame(master=self, film_id=film_id)
        self.showtimes = showtime_list

        self.film.grid(column=0, row=0, sticky='nsew')

        self.button = ctk.CTkButton(master=self, text="BOOK", command=self.book)
        self.button.grid(column=1, row=0, sticky="ns")


    def book(self):
        self.booking_function(self.film_id, self.showtimes)
