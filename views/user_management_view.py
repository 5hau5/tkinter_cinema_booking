import customtkinter as ctk
from controllers.user_controller import UserController

class UserManagementView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.controller = UserController()

        self.configure(fg_color='#282c33')
        ctk.CTkLabel(master=self,text="place holder text").pack(padx=20, pady=20)

            # Start with user table view
        self.show_user_table_view()

    def show_user_table_view(self):
        print("show_user_table_view called")
        self.switch_view(UserTableView(master=self))

    def show_add_user_view(self):
        """Switch to the ShowtimeDetailView in add_new mode."""
        self.switch_view(AddUserView(master=self))

    def switch_view(self, new_view):
        # Forget the current widgets and load the new view
        for widget in self.winfo_children():
            widget.forget()
        new_view.pack(expand=True, fill="both")

class UserTableView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        print("Initializing UserTableView")
        self.configure(fg_color='#282c33')
        self.master = master

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1), weight=0)
        self.rowconfigure((2), weight=1)

        self.initialize_user_list()

    def initialize_user_list(self):
        """Set up the user list view."""
        self.top_frame = ctk.CTkFrame(self, fg_color='#21252b')
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
        self.top_frame.columnconfigure(0, weight=1)

        # Add user button
        self.add_button = ctk.CTkButton(self.top_frame, text="Add User", command=self.master.show_add_user_view)
        self.add_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Table for displaying users
        self.table_frame = ctk.CTkScrollableFrame(self, fg_color='#282c34')
        self.table_frame.grid(row=2, column=0, sticky="nsew", padx=1, pady=1)
        self.table_frame.columnconfigure(0, weight=1)

        self.headers = ["ID", "Name", "Role", "Delete"]
        self.header_row = ctk.CTkFrame(self, fg_color='#21252b')
        self.header_row.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.header_row.grid(row=1, column=0, columnspan=4, sticky='ew', padx=10)

        for i, header in enumerate(self.headers):
            if i == 0:
                label = ctk.CTkLabel(self.header_row, text=header, anchor="w")
                label.grid(row=0, column=i, sticky='w', padx=10, pady=2)
            elif i == 1:
                label = ctk.CTkLabel(self.header_row, text=header,)
                label.grid(row=0, column=i, padx=10, pady=2)
            elif i == 3:
                label = ctk.CTkLabel(self.header_row, text=header, anchor="w")
                label.grid(row=0, column=i, sticky='e', padx=10, pady=2)
            else:
                label = ctk.CTkLabel(self.header_row, text=header, anchor="w")
                label.grid(row=0, column=i, padx=10, pady=2)

        self.load_users()

    def load_users(self):
        """Load and display users in the table."""
        self.forget_users()

        users = UserController().fetch_all_users()
        print(users)
        # Display users
        for user in users:
            row = UserRow(
                master=self.table_frame,
                user_id=user[0],
                username=user[1],
                role=user[2],
                delete_callback=self.confirm_delete_user
            )
            row.pack(fill="x", pady=2, padx=2)

    def forget_users(self):
        """Clear the currently displayed users in the table."""
        for widget in self.table_frame.winfo_children():
            if widget != self.header_row:
                widget.destroy()

    def update_user_role(self, user_id, user_role):
        UserController().add_user(user_id, user_role)

    def confirm_delete_user(self, user_id):
        """Display a confirmation dialog before deleting the user."""
        confirmation_dialog = ctk.CTkToplevel(self)
        confirmation_dialog.title("Confirm Delete")
        confirmation_dialog.geometry("300x150")

        message_label = ctk.CTkLabel(
            confirmation_dialog,
            text=f"Are you sure you want to delete user ID {user_id}?"
        )
        message_label.pack(pady=20)

        button_frame = ctk.CTkFrame(confirmation_dialog)
        button_frame.pack(pady=10)

        yes_button = ctk.CTkButton(
            button_frame,
            text="Yes",
            command=lambda: self.delete_user(confirmation_dialog, user_id)
        )
        yes_button.pack(side="left", padx=10)

        no_button = ctk.CTkButton(button_frame, text="No", command=confirmation_dialog.destroy)
        no_button.pack(side="right", padx=10)

    def delete_user(self, dialog, user_id):
        """Perform the delete operation and reload the table."""
        UserController().delete_user(user_id)
        self.load_users()
        dialog.destroy()


class UserRow(ctk.CTkFrame):
    def __init__(self, master, user_id, username, role, delete_callback):
        """
        A row representing a user in the user management table.
        
        Args:
            master: The parent widget.
            user_id (int): The ID of the user.
            username (str): The username of the user.
            role (str): The current role of the user.
        """
        super().__init__(master)
        self.master = master
        self.user_id = user_id
        self.configure(fg_color='#333842')
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')

        self.delete_callback = delete_callback

        # Display User ID and Username
        ctk.CTkLabel(master=self, text=user_id, width=100, anchor='w').grid(row=0, column=0, sticky="w", padx=10)
        ctk.CTkLabel(master=self, text=username, width=200, anchor='w').grid(row=0, column=1, padx=10)

        # Role Combobox
        self.role_combo = ctk.CTkComboBox(
            master=self,
            values=["Admin", "Staff"],  
            command=self.on_role_change,  # Triggered when a role is changed
            width=150,
            state="readonly" 
        )
        self.role_combo.set(role.capitalize())
        if role == "manager":
            self.role_combo.configure(state="disabled")

        self.role_combo.grid(row=0, column=2, padx=5)

        self.delete_button = ctk.CTkButton(self, text="DELETE", command=self.on_delete, fg_color="#ff0000", width=40)
        self.delete_button.grid(row=0, column=3, sticky='e')

    def on_role_change(self, selected_role):
        """
        Handle the change of user role via the combobox.
        
        Args:
            selected_role (str): The newly selected role.
        """
        self.master.update_user_role(self.user_id, selected_role.lower())

    def on_delete(self):
        """Invoke the delete callback for confirmation."""
        self.delete_callback(self.user_id)

        

class AddUserView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.controller = UserController() 

        self.configure(fg_color='#282c33')

        self.rowconfigure(0, weight=1) 
        self.columnconfigure(0, weight=1) 

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, pady=10, padx=10, )

        self.selected_role = None

         # Username Entry
        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Your Username")
        self.username_entry.bind('<KeyRelease>', self.update_save_button)
        self.username_entry.pack(pady=10, padx=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Your Password", show="*")
        self.password_entry.bind('<KeyRelease>', self.update_save_button)
        self.password_entry.pack(pady=10, padx=10)

        # Role Combobox
        self.role_combo = ctk.CTkComboBox(
            master=self.frame,
            values=["Staff", "Admin"], 
            command=self.on_role_change,  
            width=150,
            state="readonly"
        )

        self.role_combo.set("Staff")

        self.role_combo.pack(pady=10, padx=10)
        # Save and Back buttons
        self.button_frame = ctk.CTkFrame(self, fg_color='#202329')
        self.button_frame.rowconfigure(0, weight=0)
        self.button_frame.columnconfigure((0,1), weight=0)
        self.button_frame.grid(row=5, column=0, pady=10, padx=10)
        self.save_button = ctk.CTkButton(self.button_frame, text="SAVE", command=self.save, state="disabled", fg_color='#282c33')
        self.save_button.grid(row=0, column=1, pady=10, padx=10, sticky="e")

        self.back_button = ctk.CTkButton(self.button_frame, text="BACK", command=self.back)
        self.back_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    def on_role_change(self, event=None):
        self.selected_role = self.role_combo.get()

    def update_save_button(self, event=None):
        """
        Enable the save button if all fields are valid.
        """
        name = self.username_entry.get()  # Get the entered username
        password = self.password_entry.get()  # Get the entered password
        #  
        if (len(name) > 4 and len(password) > 5) and not any(user[1] == name for user in self.controller.fetch_all_users()):
            self.save_button.configure(state='normal', fg_color='#2e323b')
        else:
            self.save_button.configure(state='disabled', fg_color='#282c33')


    def save(self):
        """
        Save the user details to the database.
        """
        # Save cinema and screens using the controller
        self.controller.add_user(self.username_entry.get(), self.password_entry.get(), self.selected_role.lower())
        self.back()

    def back(self):
        """
        Navigate back to the cinema table view.
        """
        self.master.show_user_table_view()
