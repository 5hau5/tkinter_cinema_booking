import customtkinter as ctk
from controllers.cinema_controller import CinemaController

class CinemaManagementView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.controller = CinemaController()
        self.configure(fg_color='#282c33')

        # Start with cinema table view
        self.show_cinema_table_view()

    def show_cinema_table_view(self):
        print("show_cinema_table_view called")
        self.switch_view(CinemaTableView(master=self))

    def show_add_cinema_view(self):
        """Switch to the ShowtimeDetailView in add_new mode."""
        self.switch_view(AddCinemaView(master=self))

    def switch_view(self, new_view):
        # Forget the current widgets and load the new view
        for widget in self.winfo_children():
            widget.forget()
        new_view.pack(expand=True, fill="both")

class CinemaTableView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        print("initializing CinemaTableView")
        self.configure(fg_color='#282c33')
        self.master = master

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)

        self.initialize_cinema_list()

    def initialize_cinema_list(self):
        """Set up the cinema list view."""
        self.top_frame = ctk.CTkFrame(self, fg_color='#21252b')
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
        self.top_frame.columnconfigure(0, weight=1)

        # Add cinema button
        self.add_button = ctk.CTkButton(self.top_frame, text="Add Cinema", command=self.master.show_add_cinema_view)
        self.add_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Table for displaying cinema
        self.table_frame = ctk.CTkFrame(self, fg_color='#282c34')
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.table_frame.columnconfigure(0, weight=1)

        self.headers = ["ID", "Name", "Location", "Address",]
        self.header_row = ctk.CTkFrame(self.table_frame, fg_color='#21252b')
        self.header_row.columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.header_row.pack(fill="x", pady=2)

        # Configure the grid columns for the desired ratio
        for i, header in enumerate(self.headers):
            label = ctk.CTkLabel(self.header_row, text=header, anchor="w")
            label.grid(row=0, column=i, padx=10, pady=2, sticky='w')

        self.load_cinemas()

    def load_cinemas(self):
        """Load and display cinemas in the table with pagination."""
        self.forget_cinemas()

        cinemas = self.master.controller.fetch_all_cinemas()
        print(cinemas)
        # Display cinema
        for cinema in cinemas:
            row = CinemaRow(
                master=self.table_frame,
                cinema_id=cinema[0],
                cinema_name=cinema[1],
                city=cinema[2],
                address=cinema[3]
            )
            row.pack(fill="x", pady=2, padx=2)

    def forget_cinemas(self):
        """Clear the currently displayed cinemas in the table."""
        for widget in self.table_frame.winfo_children():
            if widget != self.header_row:
                widget.destroy()

class CinemaRow(ctk.CTkFrame):
    def __init__(self, master, cinema_id, cinema_name, city, address):
        super().__init__(master)
        self.configure(fg_color='#333842')
        self.columnconfigure((0,1,2,3), weight=1, uniform='a')
        ctk.CTkLabel(master=self, text=cinema_id, anchor="w").grid(row=0, column=0, sticky='w', padx=10)
        ctk.CTkLabel(master=self, text=cinema_name, anchor="w").grid(row=0, column=1, sticky='w', padx=10)
        ctk.CTkLabel(master=self, text=city, anchor="w").grid(row=0, column=2, sticky='w', padx=10)
        ctk.CTkLabel(master=self, text=address, anchor="w").grid(row=0, column=3, sticky='w', padx=10)
        


class AddCinemaView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.controller = CinemaController()  # Assuming CinemaController handles database operations
        self.configure(fg_color='#282c33')
        self.rowconfigure((0,1,2,4), weight=1)
        self.rowconfigure(3, weight=0)
        self.columnconfigure((0,1,2), weight=1, uniform='a')

        self.address_frame = ctk.CTkFrame(self, fg_color='#333842')
        self.address_frame.columnconfigure(0, weight=1)
        self.address_frame.grid(row=0, column=1, pady=10, padx=10, sticky="ew")


        self.address_entry = ctk.CTkEntry(master=self.address_frame, placeholder_text="Enter Address")
        self.address_entry.grid(row=0, column=0,  pady=10, padx=10, sticky="ew")
        self.address_entry.bind("<KeyRelease>", self.update_save_button)

        self.error_label = ctk.CTkLabel(master=self, text='', text_color="#ff0000")
        self.error_label.grid(row=3, column=0, columnspan=3, pady=10,)

        # Save and Back buttons
        self.button_frame = ctk.CTkFrame(self, fg_color='#202329')
        self.button_frame.rowconfigure(0, weight=0)
        self.button_frame.columnconfigure((0,1), weight=0)
        self.button_frame.grid(row=4, column=1, pady=10, padx=10)
        self.save_button = ctk.CTkButton(self.button_frame, text="SAVE", command=self.save, state="disabled")
        self.save_button.grid(row=0, column=1, pady=10, padx=10, sticky="e")

        self.back_button = ctk.CTkButton(self.button_frame, text="BACK", command=self.back)
        self.back_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Add screens in a grid layout with 3 screens per row
        self.screens = [AddScreenView(master=self, num=i + 1) for i in range(6)]

        for idx, screen in enumerate(self.screens):
            row = idx // 3  # Calculate the row number (integer division)
            column = idx % 3  # Calculate the column number (remainder)
            screen.grid(row=row + 1, column=column, pady=10, padx=10, sticky="ew")

    def update_save_button(self, event=None):
        """
        Enable the save button if all fields are valid.
        """
        all_screens_valid = all(screen.state for screen in self.screens)
        address_filled = bool(self.address_entry.get().strip())

        if all_screens_valid and address_filled:
            self.save_button.configure(state="normal")
        else:
            self.save_button.configure(state="disabled")

    def save(self):
        """
        Save the cinema details to the database and navigate back to the cinema table view.
        """
        try:
            address = self.address_entry.get().strip()

            address_parts = address.split(", ")
            if len(address_parts) < 2:
                self.error_label.configure(text="Invalid address format. Ensure it includes a street and city.")
                raise ValueError("Invalid address format. Ensure it includes a street and city.")


            # Collect screen data
            screen_data = [
                {
                    "vip_seats_cap": int(screen.vip_seats_cap.get().strip()),
                    "upper_seats_cap": int(screen.upper_seats_cap.get().strip()),
                    "lower_seats_cap": int(screen.lower_seats_cap.get().strip()),
                }
                for screen in self.screens
            ]

            # Validate screen data
            if not screen_data or not all(
                screen["vip_seats_cap"] > 0 and
                screen["upper_seats_cap"] > 0 and
                screen["lower_seats_cap"] > 0
                for screen in screen_data
            ):
                self.error_label.configure(text="All screen capacities must be positive integers.")
                raise ValueError("All screen capacities must be positive integers.")

            # Save cinema and screens using the controller
            self.controller.add_cinema(address=address, screens=screen_data)

            # Navigate back to the table view
            print("Success", "Cinema added successfully.")
            self.master.show_cinema_table_view()

        except Exception as e:
            self.error_label.configure(text= f"An error occurred while saving the cinema: {str(e)}")
            print("Error", f"An error occurred while saving the cinema: {str(e)}")

    def back(self):
        """
        Navigate back to the cinema table view.
        """
        self.master.show_cinema_table_view()


class AddScreenView(ctk.CTkFrame):
    def __init__(self, master, num):
        super().__init__(master)
        self.state = False  # Indicates if the screen input is valid
        self.columnconfigure(0, weight=1)
        self.configure(fg_color='#333842')

        ctk.CTkLabel(self, text=f"Screen {num}").grid(row=0, column=0,)

        # VIP seats
        self.vip_seats_cap = ctk.CTkEntry(self, placeholder_text="Enter VIP Seat Capacity")
        self.vip_seats_cap.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.vip_seats_cap.bind("<KeyRelease>", self.update_state)

        # Upper Hall seats
        self.upper_seats_cap = ctk.CTkEntry(self, placeholder_text="Enter Upper-Hall Seat Capacity")
        self.upper_seats_cap.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        self.upper_seats_cap.bind("<KeyRelease>", self.update_state)

        # Lower Hall seats
        self.lower_seats_cap = ctk.CTkEntry(self, placeholder_text="Enter Lower-Hall Seat Capacity")
        self.lower_seats_cap.grid(row=3, column=0, pady=10, padx=10, sticky="ew")
        self.lower_seats_cap.bind("<KeyRelease>", self.update_state)

    def update_state(self, event=None):
        """
        Update the state based on the validity of the seat capacities.
        """
        try:
            vip_valid = int(self.vip_seats_cap.get()) > 0
            upper_valid = int(self.upper_seats_cap.get()) > 0
            lower_valid = int(self.lower_seats_cap.get()) > 0
            self.state = vip_valid and upper_valid and lower_valid
        except ValueError:
            self.state = False

        # Notify parent to update the save button state
        self.master.update_save_button()




