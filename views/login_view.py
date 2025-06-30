import customtkinter as ctk
from controllers.user_controller import UserController

class LoginView(ctk.CTkFrame):
    def __init__(self, master, show_main_page):
        super().__init__(master)
        print("Initializing LoginView")

        self.user_controller = UserController()
        self.show_main_page = show_main_page
        
        # configure the grid layout and color
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)
        self.configure(fg_color='#181a1f')

        # a login frame to attach the login elements to
        self.login_frame = ctk.CTkFrame(master=self, height=20, fg_color='#202329', corner_radius=1)

        # Username Entry
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Enter Your Username")
        self.username_entry.bind('<KeyRelease>', self.update_login_button_state)
        self.username_entry.pack(pady=10, padx=10)

        # Password Entry
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Enter Your Password", show="*")
        self.password_entry.bind('<KeyRelease>', self.update_login_button_state)
        self.password_entry.pack(pady=10, padx=10)


        # Login Button
        self.login_button = ctk.CTkButton(
            master=self.login_frame,
            text="Login",
            command=self.login,
            state='disabled',
            corner_radius=1,
            fg_color='#282c33',
            width=60,
            hover_color='#323740'
        )
        
        self.login_button.pack(pady=10, padx=10)

        # Error Label (Initially Empty)
        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.error_label.pack(padx=10)

        self.login_frame.grid(row=1, column=1, padx=20, pady=20)

        self.init_skip_login()

 
    def login(self):
        print("Function login called")
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
 
        user = self.user_controller.authenticate(username, password)

        if user:
            print(f'logging in as {user[2]}')
            self.show_main_page(user)
        else:
            # Clear the fields if login fails
            self.username_entry.delete(0, 'end')  # Clear username entry
            self.password_entry.delete(0, 'end')  # Clear password entry

            # Display login failed message
            self.error_label.configure(text="Incorrect Username or Password")

    def update_login_button_state(self, event=None):
        """Enable the login button if both fields have more than 3 characters."""
        name = self.username_entry.get()  # Get the entered username
        password = self.password_entry.get()  # Get the entered password

        # Enable button if both fields have more than 3 characters
        if len(name) > 3 and len(password) > 3:
            self.login_button.configure(state='normal', fg_color='#2e323b')

        # Disable button if one of the fields is less than 3 characters
        else:
            self.login_button.configure(state='disabled', fg_color='#282c33')

    def init_skip_login(self):
        """Bypass the login for testing purposes."""

        self.skip_login_frame = ctk.CTkFrame(master=self, height=20, fg_color='#202329', corner_radius=0)

        self.button_skip_login_staff = ctk.CTkButton(master=self.skip_login_frame, text="skip as staff", command=lambda: self.skip_login("staff"), width=50)
        self.button_skip_login_admin = ctk.CTkButton(master=self.skip_login_frame, text="skip as admin", command=lambda: self.skip_login("admin"), width=50)
        self.button_skip_login_manager = ctk.CTkButton(master=self.skip_login_frame, text="skip as manager", command=lambda: self.skip_login("manager"), width=50)

        self.button_skip_login_staff.pack(pady=5,padx=5)
        self.button_skip_login_admin.pack(pady=5,padx=5)
        self.button_skip_login_manager.pack(pady=5,padx=5)

        self.skip_login_frame.grid(row=2, column=2, sticky='se')

    def skip_login(self, role):
        """Bypass the login for testing purposes."""
        print(f"Skipping login as {role}")

        if role == "manager":
            self.show_main_page((0,"manager_test","manager"))
        elif role == "admin":
            self.show_main_page((0,"admin_test","admin"))
        else:
            self.show_main_page((0,"staff_test","staff"))
