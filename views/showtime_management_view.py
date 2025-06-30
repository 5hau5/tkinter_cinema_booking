import customtkinter as ctk
from controllers.showtime_controller import ShowtimeController
from controllers.film_controller import FilmController
from controllers.cinema_controller import CinemaController
from views.film_view import FilmFrame, FilmTableView
from controllers.booking_controller import BookingController
import datetime

class ShowtimeManagementView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.controller = ShowtimeController()
        self.configure(fg_color='#282c33')

        # Start with showtime table view
        self.show_showtime_table_view()

    def show_showtime_table_view(self):
        print("show_showtime_table_view called")
        self.switch_view(ShowtimeTableView(master=self))

    def show_add_showtime(self):
        """Switch to the ShowtimeDetailView in add_new mode."""
        self.switch_view(AddShowtimeView(master=self))

    def switch_view(self, new_view):
        # Forget the current widgets and load the new view
        for widget in self.winfo_children():
            widget.forget()
        new_view.pack(expand=True, fill="both")


class ShowtimeTableView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        print("initializing ShowtimeTableView")
        self.configure(fg_color='#282c33')
        self.master = master
        self.page = 1
        self.showtimes_per_page = 10  # Number of showtimes per page

        self.controller = ShowtimeController()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

        self.initialize_showtime_list()

    def initialize_showtime_list(self):
        """Set up the showtime list view."""
        self.top_frame = ctk.CTkFrame(self, fg_color='#21252b')
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
        self.top_frame.columnconfigure(0, weight=1)

        # Search bar
        self.search_frame = ctk.CTkFrame(master=self.top_frame, fg_color='#202329')
        self.showtime_search_bar = ctk.CTkEntry(master=self.search_frame)
        self.button_search_showtime = ctk.CTkButton(
            master=self.search_frame,
            text="Search",
            command=lambda: self.search_showtime(self.showtime_search_bar.get()),
            width=40
        )
        self.search_frame.grid(column=2, row=1, sticky='se', padx=5, pady=5)
        self.showtime_search_bar.grid(column=0, row=0, sticky='se', padx=5, pady=5)
        self.button_search_showtime.grid(column=1, row=0, sticky='se', padx=5, pady=5)

        # Pagination buttons
        self.prev_page_button = ctk.CTkButton(master=self.top_frame, text='Previous Page', command=self.page_prev)
        self.next_page_button = ctk.CTkButton(master=self.top_frame, text='Next Page', command=self.page_next)
        self.prev_page_button.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.next_page_button.grid(row=1, column=1, sticky='e', padx=5, pady=5)
        self.prev_page_button.configure(state="disabled")

        self.page_label = ctk.CTkLabel(master=self.top_frame)

        # Add showtime button
        self.add_button = ctk.CTkButton(self.top_frame, text="Add Showtime", command=self.master.show_add_showtime)
        self.add_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Table for displaying showtimes
        self.table_frame = ctk.CTkFrame(self, fg_color='#282c34')
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.table_frame.columnconfigure(0, weight=1)

        self.headers = ["ID", "Film", "Screen", "Cinema", "Price", "Date", "Time", "Actions"]
        self.header_row = ctk.CTkFrame(self.table_frame, fg_color='#21252b')
        self.header_row.pack(fill="x", pady=2)

        # Configure the grid columns with minsize and weight
        column_settings = [
            {"minsize": 40, "weight": 1},   # ID column
            {"minsize": 260, "weight": 10}, # Film column
            {"minsize": 20, "weight": 2},   # Screen column
            {"minsize": 130, "weight": 5}, # Cinema column
            {"minsize": 10, "weight": 2},   # Price column
            {"minsize": 70, "weight": 3},   # Date column
            {"minsize": 80, "weight": 2},   # Time column
            {"minsize": 80, "weight": 8},   # Actions column
        ]

        for i, settings in enumerate(column_settings):
            self.header_row.columnconfigure(i, minsize=settings["minsize"], weight=settings["weight"])

        # Add headers to the grid
        for i, header in enumerate(self.headers):
            label = ctk.CTkLabel(self.header_row, text=header, anchor="w")
            label.grid(row=0, column=i, sticky="w", padx=10, pady=2)


        self.load_showtimes()

    def load_showtimes(self, search_text=None):
        """Load and display showtimes in the table with pagination."""
        self.forget_showtimes()
        offset = (self.page - 1) * self.showtimes_per_page
        showtimes = self.master.controller.fetch_showtimes(search_text, limit=self.showtimes_per_page, offset=offset)
        print(showtimes)
        # Display showtimes
        for showtime in showtimes:
            row = ShowtimeRow(
                master=self.table_frame,
                showtime_id=showtime[0],
                film_name=showtime[1],
                screen_name=showtime[3],
                cinema_name=showtime[5],
                price_lower=showtime[8],
                date=showtime[6],
                time=showtime[7]
            )
            row.pack(fill="x", pady=2, padx=2)

        # Update button states
        self.next_page_button.configure(state="normal" if len(showtimes) == self.showtimes_per_page else "disabled")
        self.prev_page_button.configure(state="normal" if self.page > 1 else "disabled")

    def search_showtime(self, search_text=None):
        """Handle search functionality."""
        self.page = 1
        self.load_showtimes(search_text)

    def page_next(self):
        """Load the next page of showtimes."""
        self.page += 1
        self.load_showtimes(self.showtime_search_bar.get())

    def page_prev(self):
        """Load the previous page of showtimes."""
        if self.page > 1:
            self.page -= 1
            self.load_showtimes(self.showtime_search_bar.get())

    def forget_showtimes(self):
        """Clear the currently displayed showtimes in the table."""
        for widget in self.table_frame.winfo_children():
            if widget != self.header_row:
                widget.destroy()

    def handle_delete_showtime(self, showtime_id):
        """Display confirmation dialog and handle deletion."""
        confirmation_dialog = ctk.CTkToplevel(self)
        confirmation_dialog.title("Confirm Delete")
        confirmation_dialog.geometry("300x150")

        message_label = ctk.CTkLabel(
            confirmation_dialog,
            text=f"Are you sure you want to delete showtime ID {showtime_id}?"
        )
        message_label.pack(pady=20)

        button_frame = ctk.CTkFrame(confirmation_dialog)
        button_frame.pack(pady=10)

        yes_button = ctk.CTkButton(
            button_frame,
            text="Yes",
            command=lambda: self.confirm_delete_showtime(confirmation_dialog, showtime_id)
        )
        yes_button.pack(side="left", padx=10)

        no_button = ctk.CTkButton(button_frame, text="No", command=confirmation_dialog.destroy)
        no_button.pack(side="right", padx=10)

    def confirm_delete_showtime(self, dialog, showtime_id):
        """Perform the delete operation and reload the table."""
        self.controller.delete_showtime(showtime_id)
        print(f"Showtime ID {showtime_id} deleted successfully.")
        self.load_showtimes()  # Reload the showtime table
        dialog.destroy()

class ShowtimeRow(ctk.CTkFrame):
    def __init__(self, master, showtime_id, film_name, screen_name, cinema_name, price_lower, date, time):
        super().__init__(master)
        self.configure(fg_color='#333842')
        self.master = master
        # Configure columns for the ShowtimeRow with minsize and weight
        row_column_settings = [
            {"minsize": 30, "weight": 3},   # ID column
            {"minsize": 350, "weight": 10}, # Film column
            {"minsize": 40, "weight": 2},   # Screen column
            {"minsize": 180, "weight": 6}, # Cinema column
            {"minsize": 30, "weight": 3},   # Price column
            {"minsize": 50, "weight": 5},   # Date column
            {"minsize": 30, "weight": 3},   # Time column
            {"minsize": 80, "weight": 8},   # Actions column
        ]

        for i, settings in enumerate(row_column_settings):
            self.columnconfigure(i, minsize=settings["minsize"], weight=settings["weight"])

        self.showtime_id = showtime_id

        # Display showtime details
        fields = [showtime_id, film_name, screen_name, cinema_name, price_lower, date, time]
        for i, field in enumerate(fields):
            label = ctk.CTkLabel(self, text=field, anchor="w")
            label.grid(row=0, column=i, sticky="ew", padx=10, pady=2)


        # Delete button
        delete_button = ctk.CTkButton(self, text="DEL", fg_color="#AA4423", command=self.delete_showtime, state="disabled")
        if BookingController().fetch_all_bookings_by_showtime_id(showtime_id):
            delete_button.configure(state="normal", fg_color="red")

        delete_button.grid(row=0, column=len(fields), padx=10, pady=2, sticky='ew')

    def delete_showtime(self):
        """Delegate deletion to the parent view."""
        self.master.master.handle_delete_showtime(self.showtime_id)



class AddShowtimeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='#282c33')
        self.master = master

        self.film_controller = FilmController()
        self.cinema_controller = CinemaController()
        self.showtime_controller = ShowtimeController()

        self.select_film_frame = ctk.CTkFrame(master=self)

        self.selected_film = None
        self.selected_cinema = None
        self.selected_screen = None

        self.rowconfigure((0, 1, 2, 3), weight=0)
        self.columnconfigure((0, 1, 2), weight=1)

        # Initialize frame elements
        self.init_frame_elements()

    def init_frame_elements(self):
        """Initialize elements for adding a showtime."""
        self.clear_elements()

        # Film selection
        self.select_film_button = ctk.CTkButton(self, text="Select Film", command=self.select_film_view)
        self.select_film_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Cinema selection dropdown


        self.cinemas = self.cinema_controller.fetch_all_cinemas()
        self.cinema_dropdown = ctk.CTkComboBox(
            self, values=["Select a Cinema"] + [cinema[1] for cinema in self.cinemas], command=self.update_screens
        )
        self.cinema_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.screen_dropdown = ctk.CTkComboBox(self, values=["Select a Screen"])
        self.screen_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Date entry

        self.date_entry = ctk.CTkEntry(self, placeholder_text='YYYY-MM-DD')
        self.date_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.date_entry.insert(0, datetime.date.today().strftime('%Y-%m-%d'))  # Default to today

        self.time_dropdown = ctk.CTkComboBox(self, values=["09:00", "13:00", "17:00", "23:00"])
        self.time_dropdown.grid(row=5, column=1, padx=10, pady=10, sticky="ew")


        # Date entry
        self.price_entry = ctk.CTkEntry(self, placeholder_text="Lower Seat Price")
        self.price_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Save Button
        self.button_frame = ctk.CTkFrame(self, fg_color='#202329')
        self.button_frame.rowconfigure(0, weight=0)
        self.button_frame.columnconfigure((0,1), weight=0)
        self.button_frame.grid(row=6, column=1, pady=10, padx=10)

        self.save_button = ctk.CTkButton(self.button_frame, text="Save", command=self.save_showtime)
        self.save_button.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        self.back_button = ctk.CTkButton(self.button_frame, text="Back", command=self.master.show_showtime_table_view)
        self.back_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Error Message Label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=7, column=0, columnspan=4, pady=10)

    def select_film_view(self):
        """Switch to FilmTableView to select a film."""
        if not hasattr(self, 'select_film_frame') or not self.select_film_frame.winfo_exists():
            self.select_film_frame = ctk.CTkFrame(self)
        
        self.select_film_frame.grid(row=0, column=0, rowspan=6, columnspan=4, sticky="nsew")
        self.film_table = FilmTableView(
            master=self.select_film_frame,
            select_film=True,
            on_film_select=self.on_film_selected
        ).pack(expand=True, fill="both")

    def on_film_selected(self, film_id):
        """Handle film selection and return to AddShowtimeView."""
        self.selected_film = self.film_controller.fetch_film_by_id(film_id=film_id)
        if hasattr(self, 'select_film_frame') and self.select_film_frame.winfo_exists():
            self.select_film_frame.grid_forget()  # Hide the film selection view
        self.init_frame_elements()  # Refresh the main view


    def update_screens(self, selected_cinema_name):
        """Update the screen dropdown based on the selected cinema."""
        selected_cinema = next((cinema for cinema in self.cinemas if cinema[1] == selected_cinema_name), None)
        if selected_cinema:
            self.selected_cinema = selected_cinema
            cinema_id = selected_cinema[0]  # Assuming cinema ID is at index 0
            screens = self.cinema_controller.fetch_screens_by_cinema(cinema_id)
            self.screen_dropdown.configure(values=[f"{screen[1]}" for screen in screens])  # Assuming screen_number is at index 1
        else:
            self.screen_dropdown.configure(values=[])
            self.selected_screen = None

    def save_showtime(self):
        """Save the showtime to the database."""
        try:
            # Ensure the selected film, cinema, screen, date, and time are valid
            if not self.selected_film:
                self.error_label.configure(text="Error: No film selected!")
                return

            if not self.selected_cinema:
                self.error_label.configure(text="Error: No cinema selected!")
                return

            selected_screen = self.screen_dropdown.get()
            print(selected_screen)
            if not selected_screen or "Screen" not in selected_screen:
                self.error_label.configure(text="Error: No valid screen selected!")
                return

            selected_date = self.date_entry.get()
            selected_time = self.time_dropdown.get()
            selected_price = self.price_entry.get()

            # Validate required fields
            if not (selected_date and selected_time and selected_price):
                self.error_label.configure(text="Error: All fields must be filled!")
                return

            # Validate date format
            try:
                selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
                today = datetime.date.today()
                valid_start_date = today + datetime.timedelta(days=1)  # Tomorrow
                valid_end_date = today + datetime.timedelta(days=31)  # 30 days from tomorrow

                if not (valid_start_date <= selected_date < valid_end_date):
                    raise ValueError
            except ValueError:
                self.error_label.configure(text="Error: Invalid date! Must be within the next 30 days (excluding today).")
                return

            # Validate price
            try:
                selected_price = int(selected_price)
            except ValueError:
                self.error_label.configure(text="Error: Price must be a valid number!")
                return

            # Map screen number to screen ID
            cinema_id = self.selected_cinema[0]  # Assuming cinema ID is at index 0
            screens = self.cinema_controller.fetch_screens_by_cinema(cinema_id)
            print(screens)
            screen_id = None
            for screen in screens:
                if selected_screen == screen[1]:  # Compare dropdown text with screen tuple's name (e.g., "Screen [n]")
                    screen_id = screen[0]  # Get the corresponding screen_id
                    break

            if screen_id is None:
                self.error_label.configure(text="Error: Selected screen not found!")
                return

            # Save the showtime
            self.showtime_controller.add_showtime(
                film_id=self.selected_film[0],  # Assuming film ID is at index 0
                screen_id=screen_id,
                date=selected_date.strftime('%Y-%m-%d'),
                time=selected_time,
                price_lower=selected_price,
                price_upper=int(selected_price * 1.2),
                vip_price=int(selected_price * 1.4)
            )

            print("Showtime added successfully!")
            self.master.show_showtime_table_view()

        except Exception as e:
            self.error_label.configure(text=f"Error saving showtime: {e}")


    def clear_elements(self):
        """Clear all existing elements to avoid duplicates."""
        for widget in self.winfo_children():
            widget.destroy()




if __name__ == "__main__":
    root = ctk.CTk()
    ShowtimeManagementView(master=root).pack(fill="both", expand=True)
    root.mainloop()
