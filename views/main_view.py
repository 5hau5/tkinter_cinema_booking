import customtkinter as ctk
from views.film_view import FilmView
from views.bookings_view import BookingView
from views.film_listing_view import FilmListingView
from views.home_view import HomeView
from views.showtime_management_view import ShowtimeManagementView
from views.user_management_view import UserManagementView
from views.cinema_management_view import CinemaManagementView
from views.create_reports_view import CreateReportView

class MainView(ctk.CTkFrame):
    def __init__(self, master, cinema_id, user_detail):
        """
        Initialize the main view.
        :param master: Parent window.
        :param user_role: Role of the current user (e.g., 'staff', 'admin', 'manager').
        """
        super().__init__(master)
        self.user_name = user_detail[1]
        self.user_id = user_detail[0]
        self.user_role = user_detail[2]

        self.cinema_id = cinema_id

        self.rowconfigure(0, minsize=50)
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0), weight=1, uniform='a') 

        # Navigation frame for navigation buttons
        self.nav_frame = ctk.CTkFrame(master=self, corner_radius=0, fg_color='#181a1f')
        #self.nav_frame.columnconfigure(0, minsize=60)
        self.nav_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        #self.nav_frame.columnconfigure((0, 1, 2), weight=0)
        self.nav_frame.rowconfigure((0), weight=1,)
        self.nav_frame.grid(row=0, columnspan=1, padx=0, pady=0, sticky='nsew')

        self.home_button = ctk.CTkButton(master=self.nav_frame, 
                                         text="Home", 
                                         command=self.show_home_view, 
                                         state='normal', 
                                         corner_radius=0, 
                                         width=60, 
                                         fg_color='#282c33', 
                                         text_color_disabled='#FFFFFF', 
                                         hover_color="#22252b", 
                                         text_color='#adadad') 

        self.film_button = ctk.CTkButton(master=self.nav_frame, 
                                         text="Films", 
                                         command=self.show_film_view, 
                                         state='normal', 
                                         corner_radius=0, 
                                         fg_color='#202329', 
                                         text_color_disabled='#FFFFFF', 
                                         hover_color="#22252b", 
                                         text_color='#adadad') 

        self.filmls_button = ctk.CTkButton(master=self.nav_frame, 
                                         text="Film Listings", 
                                         command=self.show_film_listing_view, 
                                         state='normal', 
                                         corner_radius=0, 
                                         fg_color='#202329', 
                                         text_color_disabled='#FFFFFF', 
                                         hover_color="#22252b", 
                                         text_color='#adadad') 
        
        self.showtime_button = ctk.CTkButton(master=self.nav_frame, 
                                         text="Showtime Management", 
                                         command=self.show_showtime_management_view, 
                                         state='normal', 
                                         corner_radius=0, 
                                         fg_color='#202329', 
                                         text_color_disabled='#FFFFFF', 
                                         hover_color="#22252b", 
                                         text_color='#adadad') 
        self.bookings_button = ctk.CTkButton(master=self.nav_frame, 
                                         text="Bookings", 
                                         command=self.show_bookings_view, 
                                         state='normal', 
                                         corner_radius=0, 
                                         fg_color='#202329', 
                                         text_color_disabled='#FFFFFF', 
                                         hover_color="#22252b", 
                                         text_color='#adadad') 
        self.user_management_button = ctk.CTkButton(master=self.nav_frame, 
                                         text="User Management", 
                                         command=self.show_user_management_view, 
                                         state='normal', 
                                         corner_radius=0, 
                                         fg_color='#202329', 
                                         text_color_disabled='#FFFFFF', 
                                         hover_color="#22252b", 
                                         text_color='#adadad') 
        
        self.cinema_management_button = ctk.CTkButton(master=self.nav_frame, 
                                         text="Cinema Management", 
                                         command=self.show_cinema_management_view, 
                                         state='normal', 
                                         corner_radius=0, 
                                         fg_color='#202329', 
                                         text_color_disabled='#FFFFFF', 
                                         hover_color="#22252b", 
                                         text_color='#adadad') 
        self.create_reports_button = ctk.CTkButton(master=self.nav_frame, 
                                         text="Create Reports", 
                                         command=self.show_create_reports_view, 
                                         state='normal', 
                                         corner_radius=0, 
                                         fg_color='#202329', 
                                         text_color_disabled='#FFFFFF', 
                                         hover_color="#22252b", 
                                         text_color='#adadad') 
        
        self.nav_buttons = [
            self.home_button, 
            self.filmls_button,
            self.bookings_button,

                            ]
        
        self.nav_buttons_admin = [
            self.film_button, 
            self.showtime_button,
            self.create_reports_button,

        ]

        self.nav_buttons_manager = [
            self.user_management_button,
            self.cinema_management_button,
        ]

        if self.user_role == 'admin':
            self.nav_buttons += self.nav_buttons_admin

        if self.user_role == 'manager':
            self.nav_buttons += self.nav_buttons_admin + self.nav_buttons_manager
        
        # Place buttons in the grid
        for i, button in enumerate(self.nav_buttons):
            button.grid(row=0, column=i, sticky='nsew', padx=1)

        self.content_frame = ctk.CTkFrame(self, fg_color='#282c33')  # Main content area
        self.content_frame.grid(row=1, columnspan=3, rowspan=3, padx=0, pady=0, sticky='nsew')

        self.show_home_view()

            
    def show_home_view(self):
        """
        Show the home view (available to all users).
        """
        self.switch_view(HomeView(self.content_frame, self.user_name, self.user_role), self.home_button)    

    def show_film_view(self):
        """
        Show the film view (only for admins, managers).
        """
        self.switch_view(FilmView(self.content_frame), self.film_button)

    def show_film_listing_view(self):
        """
        Show the film listing view (available to all users).
        """
        self.switch_view(FilmListingView(self.content_frame, self.user_role, self.cinema_id, self.user_id), self.filmls_button)

    def show_showtime_management_view(self):
        """
        Show the showtime view (only for admins, managers).
        """
        self.switch_view(ShowtimeManagementView(self.content_frame), self.showtime_button)

    def show_bookings_view(self):
        """
        Show the showtime view (only for admins, managers).
        """
        self.switch_view(BookingView(self.content_frame, self.cinema_id, self.user_role), self.bookings_button)

    def show_user_management_view(self):
        """
        Show the user management view (only for managers).
        """
        self.switch_view(UserManagementView(self.content_frame), self.user_management_button)

    def show_cinema_management_view(self):
        """
        Show the cinema management view (only for managers).
        """
        self.switch_view(CinemaManagementView(self.content_frame), self.cinema_management_button)

    def show_create_reports_view(self):
        """
        Show the create reports view (only for admins, managers).
        """
        self.switch_view(CreateReportView(self.content_frame, self.cinema_id), self.create_reports_button)

    def switch_view(self, new_view, button_pressed):
        """
        Replace the current content in the content_frame with the new view.
        Disable the pressed button and Enable the released button
        :param new_view: The new view to display.
        :pram button_pressed: The button to be diabled
        """
        # Disable the currently pressed button and enable the previously pressed button
        button_pressed.configure(state='disabled', fg_color='#282c33')

        # Disable the pressed button and re-enable the others
        for button in self.nav_buttons:
            if button != button_pressed:
                button.configure(state='normal', fg_color='#202329') 

        # forget the stuff in the content frame and load a the new view in it
        for widget in self.content_frame.winfo_children():
            widget.forget()
            widget.forget()
        new_view.pack(expand=True, fill="both")


# Example usage
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    # Pass 'admin', 'manager', or 'staff' to test different role-specific functionality
    MainView(app, user_role="admin").pack(expand=True, fill="both")
    app.mainloop()
