import customtkinter as ctk
from tkinter.messagebox import showerror, showinfo
from controllers.film_controller import FilmController


class FilmManagementView(ctk.CTkFrame):
    def __init__(self, master, user_role):
        """
        Initialize the Film Management View.

        Parameters:
        - master: The parent widget.
        - user_role (str): The role of the currently logged-in user. Only 'Admin' is allowed to manage films.
        """
        super().__init__(master)

        # Restrict access to Admins only
        if user_role != "Admin":
            showerror("Access Denied", "Only Admins can manage films.")
            self.destroy()  # Close the frame if access is denied
            return

        self.controller = FilmController()

        # Widgets for Film Management
        self.title_label = ctk.CTkLabel(self, text="Film Title:")
        self.title_entry = ctk.CTkEntry(self, placeholder_text="Enter film title")

        self.add_button = ctk.CTkButton(self, text="Add Film", command=self.add_film)
        self.delete_button = ctk.CTkButton(self, text="Delete Film", command=self.delete_film)

        # Layout the widgets
        self.title_label.pack(pady=10)
        self.title_entry.pack(pady=10)
        self.add_button.pack(pady=10)
        self.delete_button.pack(pady=10)

    def add_film(self):
        """
        Add a new film to the system.
        """
        title = self.title_entry.get().strip()  # Get and trim the input title
        if title:
            try:
                success = self.controller.add_film(title)  # Add logic in FilmController
                if success:
                    showinfo("Success", f"Film '{title}' added successfully!")
                else:
                    showerror("Error", f"Failed to add the film '{title}'. It may already exist.")
            except Exception as e:
                showerror("Error", f"An error occurred while adding the film: {str(e)}")
        else:
            showerror("Validation Error", "Film title is required to add a film.")

    def delete_film(self):
        """
        Delete an existing film from the system.
        """
        title = self.title_entry.get().strip()  # Get and trim the input title
        if title:
            try:
                success = self.controller.delete_film(title)  # Add logic in FilmController
                if success:
                    showinfo("Success", f"Film '{title}' deleted successfully!")
                else:
                    showerror("Error", f"Film '{title}' could not be found or deleted.")
            except Exception as e:
                showerror("Error", f"An error occurred while deleting the film: {str(e)}")
        else:
            showerror("Validation Error", "Film title is required to delete a film.")
