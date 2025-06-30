import customtkinter as ctk

class HomeView(ctk.CTkFrame):
    def __init__(self, master, user_name, user_role):
        """
        Initialize the Home View.

        Parameters:
        - master: The parent widget.
        - user_name: The username of the logged-in user.
        - user_role: The role of the logged-in user.
        """
        super().__init__(master)
        self.master = master  # Reference to the App instance
        self.user_name = user_name
        self.user_role = user_role

        self.configure(fg_color="#282c33")

        # Title
        ctk.CTkLabel(
            self,
            text="Horizon Cinema Booking System",
            font=("Arial", 24, "bold"),
            text_color="white",
        ).pack(pady=20)

        # User Info
        ctk.CTkLabel(
            self,
            text=f"Logged in as: {self.user_name} ({self.user_role})",
            font=("Arial", 16),
            text_color="lightgray",
        ).pack(pady=10)

        # Logout Button
        ctk.CTkButton(
            self,
            text="Logout",
            command=self.logout_handler,
            fg_color="#FF6347",
            text_color="white",
        ).pack(pady=20)

    def logout_handler(self):
        """
        Handle logout button click.
        """
        print(f"User {self.user_name} logged out.")
        self.master.master.master.load_login_page()  # Call App's method to load the login page
