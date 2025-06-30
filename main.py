import customtkinter as ctk
from views.login_view import LoginView
from views.main_view import MainView
import configparser

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1300x720")
        self.minsize(1300, 720)  # Set the minimum size of the window
        self.title("Cinema Booking System")

        self.initialize_cinema()

        # Start with the login view
        self.login_view = LoginView(self, self.load_main_page)
        self.login_view.pack(expand=True, fill="both")
        self.bind_all("<Button-1>", self.set_focus)

    def initialize_cinema(self):
        """Initialize self.cinema_id by reading from a .ini file."""
        config = configparser.ConfigParser()
        try:
            # Read the .ini file
            config.read("settings.ini")
            
            # Extract cinema_id from the [DEFAULT] section
            self.cinema_id = int(config.get("DEFAULT", "cinema_id"))
            print(f"Cinema ID initialized to: {self.cinema_id}")
        except (configparser.Error, KeyError, ValueError) as e:
            # Handle errors such as missing key or invalid format
            print(f"Error reading cinema_id from settings.ini: {e}")
            self.cinema_id = 1  # Default fallback
            print(f"Default Cinema ID set to: {self.cinema_id}")

    def load_main_page(self, user_detail):
        """
        Load the main application view after successful login.
        """
        self.login_view.pack_forget()
        self.main_view = MainView(self, self.cinema_id, user_detail)
        self.main_view.pack(expand=True, fill="both")

    def load_login_page(self):
        """
        Load the login view after logout.
        """
        if hasattr(self, 'main_view'):
            self.main_view.pack_forget()
        self.login_view = LoginView(self, self.load_main_page)
        self.login_view.pack(expand=True, fill="both")


    def set_focus(self, event):
        """Set focus to the clicked widget if possible."""
        try:
            event.widget.focus_set()  # Set focus to the clicked widget
        except AttributeError:
            pass  # If the widget does not support focus_set, do nothing

if __name__ == "__main__":
    app = App()
    app.mainloop()
