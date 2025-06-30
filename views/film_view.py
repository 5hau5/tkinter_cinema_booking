import customtkinter as ctk
from controllers.film_controller import FilmController
from PIL import Image, ImageTk
from PIL import ImageOps
import io

#['#181a1f', '#21252b', '#282c34', '#333842'] 

class FilmView(ctk.CTkFrame):
    def __init__(self, master):
        """
        Initialize the FilmView.
        :param master: Parent frame.
        """
        super().__init__(master)
        self.master = master
        self.controller = FilmController()
        self.configure(fg_color='#282c33')

        # Start with film table view
        self.show_film_table_view()

    def show_film_table_view(self):
        print("show_film_table_view called")
        self.switch_view(FilmTableView(master=self))

    def show_film_detail_view(self, film_id=None):
        """Show the FilmDetailView for either viewing/editing or adding a new film."""
        print("show_film_detail_view called")
        self.switch_view(FilmDetailView(master=self, film_id=film_id))


    def switch_view(self, new_view):
        # forget the stuff in the content frame and load a the new view in it
        for widget in self.winfo_children():
            widget.forget()
        new_view.pack(expand=True, fill="both")

class FilmTableView(ctk.CTkFrame):
    def __init__(self, master, select_film=False, on_film_select=None):
        super().__init__(master)
        print("initializing FilmTableView")
        self.configure(fg_color='#282c33')
        self.master = master
        self.controller = FilmController()
        self.page = 1
        self.films_per_page = 10  # Number of films per page

        self.is_select_film = select_film
        self.on_film_select = on_film_select
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0), weight=0)

        self.initialize_film_list()

    def initialize_film_list(self):
        """Set up the film list view."""
        self.top_frame = ctk.CTkFrame(self, fg_color='#21252b')
        self.top_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)
        self.top_frame.columnconfigure(0, weight=1)

        # Search bar
        self.search_frame = ctk.CTkFrame(master=self.top_frame, fg_color='#202329')
        self.film_search_bar = ctk.CTkEntry(master=self.search_frame)
        self.button_search_film = ctk.CTkButton(master=self.search_frame, text="Search",
                                                command=lambda: self.search_film(self.film_search_bar.get()), width=40)
        self.search_frame.grid(column=2, row=1, sticky='se', padx=5, pady=5)
        self.film_search_bar.grid(column=0, row=0, sticky='se', padx=5, pady=5)
        self.button_search_film.grid(column=1, row=0, sticky='se', padx=5, pady=5)

        # Pagination buttons
        self.prev_page_button = ctk.CTkButton(master=self.top_frame, text='Previous Page', command=self.page_prev)
        self.next_page_button = ctk.CTkButton(master=self.top_frame, text='Next Page', command=self.page_next)
        self.prev_page_button.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.next_page_button.grid(row=1, column=1, sticky='e', padx=5, pady=5)
        self.prev_page_button.configure(state="disabled")

        self.page_label = ctk.CTkLabel(master=self.top_frame)

        # Add film button
        if not self.is_select_film:
            self.add_button = ctk.CTkButton(self.top_frame, text="Add Film", command=self.show_add_film)
            self.add_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Table for displaying films
        self.table_frame = ctk.CTkFrame(self, fg_color='#282c34')
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.table_frame.columnconfigure(0, weight=1)

        self.headers = ["ID", "Title", "Actions"]
        self.header_row = ctk.CTkFrame(self.table_frame, fg_color='#21252b')
        self.header_row.pack(fill="x", pady=2)

        # Configure the grid columns with minsize and weight
        column_settings = [
            {"minsize": 60, "weight": 1},   # ID column
            {"minsize": 550, "weight": 5}, # Title column
            {"minsize": 100, "weight": 2},  # Actions column
        ]

        for i, settings in enumerate(column_settings):
            self.header_row.columnconfigure(i, minsize=settings["minsize"], weight=settings["weight"])

        # Add headers to the grid
        for i, header in enumerate(self.headers):
            label = ctk.CTkLabel(self.header_row, text=header, anchor="w")
            label.grid(row=0, column=i, sticky="w", padx=10, pady=2)

            

        self.load_films()

    def load_films(self, search_text=None):
        """Load and display films in the table with pagination."""
        self.forget_films()
        # Clear existing rows
        for widget in self.table_frame.winfo_children():
            if widget != self.header_row:
                widget.destroy()

        # Fetch paginated films
        offset = (self.page - 1) * self.films_per_page
        films = self.controller.fetch_all_films(search_text, limit=self.films_per_page, offset=offset)

        # Display films
        for film in films:
            row = FilmRow(master=self.table_frame, film_id=film[0], film_title=film[1], select_film=self.is_select_film)
            row.pack(fill="x", pady=2, padx=2)

        # Update button states
        self.next_page_button.configure(state="normal" if len(films) == self.films_per_page else "disabled")
        self.prev_page_button.configure(state="normal" if self.page > 1 else "disabled")

    def search_film(self, search_text=None):
        """Handle search functionality."""
        self.page = 1
        self.load_films(search_text)

    def page_next(self):
        """Load the next page of films."""
        self.page += 1
        self.load_films(self.film_search_bar.get())

    def page_prev(self):
        """Load the previous page of films."""
        if self.page > 1:
            self.page -= 1
            self.load_films(self.film_search_bar.get())

    def forget_films(self):
        """Clear the currently displayed films in the table."""
        for widget in self.table_frame.winfo_children():
            # Ensure the header row is not removed
            if widget != self.header_row:
                widget.destroy()

    def show_add_film(self):
        """Switch to the FilmDetailView in add_new mode."""
        self.master.show_film_detail_view(film_id=None)

    def show_film_detail_view(self, film_id):
        self.master.show_film_detail_view(film_id)

    def back_to_add_showtime_view(self, film_id):
        self.on_film_select(film_id)


class FilmRow(ctk.CTkFrame):
    def __init__(self, master, film_id, film_title, select_film=False):
        """
        Initialize the EditFilmView.
        :param master: Parent frame.
        """
        super().__init__(master)
        self.configure(fg_color='#333842')
        self.columnconfigure(0, weight=1)  # ID column
        self.columnconfigure(1, weight=17)  # Title column
        self.columnconfigure(2, weight=6)  # Actions column

        self.is_select_film = select_film

        self.master_table = master
        self.film_id = film_id

        # Configure columns for the FilmRow with minsize and weight
        row_column_settings = [
            {"minsize": 50, "weight": 1},   # ID column
            {"minsize": 250, "weight": 5}, # Title column
            {"minsize": 100, "weight": 2},  # Actions column
        ]

        for i, settings in enumerate(row_column_settings):
            self.columnconfigure(i, minsize=settings["minsize"], weight=settings["weight"])

        self.film_id_label = ctk.CTkLabel(master=self, text=film_id, anchor='w')
        self.film_id_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        self.film_title_label = ctk.CTkLabel(master=self, text=film_title, anchor='w')
        self.film_title_label.grid(row=0, column=1, sticky="w", padx=10, pady=2)

        self.button_frame = ctk.CTkFrame(master=self, fg_color='#282c34')
        if self.is_select_film:
            self.select_button = ctk.CTkButton(master=self.button_frame, text="SELECT", command= self.select_film)
            self.select_button.grid(row=0, column=0, padx=5, pady=1)
        else:
            self.view_button = ctk.CTkButton(master=self.button_frame, text="VIEW", command= self.view_film)
            self.view_button.grid(row=0, column=0, padx=5, pady=1)
            self.delete_button = ctk.CTkButton(master=self.button_frame, text="DEL", fg_color="red", command=self.delete_film)
            self.delete_button.grid(row=0, column=1, padx=5, pady=1)
        self.button_frame.grid(row=0, column=2, padx=10, pady=2, sticky='e')
    
    def select_film(self):
        self.master.master.back_to_add_showtime_view(self.film_id)

    def view_film(self):
        self.master.master.show_film_detail_view(self.film_id)

    def delete_film(self):
        """Handle deleting a film."""
        # Create a confirmation dialog with Yes/No buttons
        confirmation_dialog = ctk.CTkToplevel(self)
        confirmation_dialog.title("Confirm Delete")
        confirmation_dialog.geometry("300x150")

        # Confirmation message
        message_label = ctk.CTkLabel(confirmation_dialog, text=f"Are you sure you want to delete film ID {self.film_id}?")
        message_label.pack(pady=20)

        # Yes and No buttons
        button_frame = ctk.CTkFrame(confirmation_dialog)
        button_frame.pack(pady=10)

        yes_button = ctk.CTkButton(button_frame, text="Yes", command=lambda: self.confirm_delete(confirmation_dialog))
        yes_button.pack(side="left", padx=10)

        no_button = ctk.CTkButton(button_frame, text="No", command=confirmation_dialog.destroy)
        no_button.pack(side="right", padx=10)

    def confirm_delete(self, dialog):
        """Perform the delete operation and close the dialog."""
        controller = self.master_table.master.master.controller
        if controller.delete_film(self.film_id):
            print(f"Film ID {self.film_id} deleted successfully.")
            self.master_table.load_films()  # Reload the film table
        else:
            print(f"Failed to delete film ID {self.film_id}.")
        dialog.destroy()
        self.master_table.load_films()


class FilmDetailView(ctk.CTkFrame):
    def __init__(self, master, film_id=None):
        super().__init__(master)
        self.configure(fg_color='#282c33')
        self.master = master
        self.original_film_data = None  # To store original data for canceling changes

        self.rowconfigure((0,1,2,3), weight=1)
        self.columnconfigure((0,1), weight=1)


        # Determine mode
        if film_id:
            self.mode = "view"
            self.film = master.controller.fetch_film_by_id(film_id)
            self.original_film_data = list(self.film)  # Save original data
        else:
            self.mode = "add_new"
            self.film = [None, "", "", "", "", "", ""]  # Initialize empty film data

        # Initialize frame elements
        self.init_frame_elements()

        # Initialize buttons
        self.init_buttons()

        # Set mode-specific behavior
        self.update_mode()

    def init_frame_elements(self):
        """Set up the film details view with all elements."""
        self.clear_elements()  # Ensure no duplicate elements

        # Column 1: Button for adding a film image
        # Check if blob data (image) exists in self.film[5]
        if self.film[6]:  # Assuming self.film[5] contains the blob data
            # Convert the blob data to an image
            image_blob = io.BytesIO(self.film[6])
            loaded_image = Image.open(image_blob)
            # Resize the image to fit the button (150x200)
            resized_image = ImageOps.fit(loaded_image, (150, 200), method=Image.Resampling.LANCZOS)
            # Convert to PhotoImage for CTkButton
            photo_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(150, 200))

            self.button_film_image = ctk.CTkButton(
                self,
                text='',  # No text if the image is displayed
                command=self.select_image,
                image=photo_image,
                height=200, width=150,
                fg_color='#282c33',
                hover_color='#323740'
            )
        else:
            # Default button when no image is available
            self.button_film_image = ctk.CTkButton(
                self,
                text='+Add Image',
                command=self.select_image,
                height=200, width=150,
                fg_color='#282c33',
                hover_color='#323740'
            )
        self.button_film_image.grid(row=1, column=0, rowspan=2, padx=10, pady=10)

        # Column 2: Frame for film details
        self.details_frame = ctk.CTkFrame(self, fg_color='#21252b')
        self.details_frame.grid(row=3, column=0, columnspan=2, rowspan=1, padx=10, pady=10)
        self.details_frame.columnconfigure((0,1,2,3,4,5), weight=1)

        # Film title
        self.film_title_textbox = ctk.CTkTextbox(self, wrap="char", height=40, fg_color='#323740')
        self.film_title_textbox.insert("0.0", self.film[1])  # Assuming title is at index 1
        self.film_title_textbox.grid(row=1, column=1, sticky='ew', pady=10, padx=10)

        # Film age rating
        self.age_rating_label = ctk.CTkLabel(self.details_frame, text='Rating:', width=60)
        self.age_rating_label.grid(row=0, column=2, padx=10, pady=2, sticky="ew")

        # Dropdown options for age ratings
        age_rating_options = [
            "G",          # General audiences
            "PG",         # Parental guidance suggested
            "PG-13",      # Parents strongly cautioned
            "R",          # Restricted
            "NC-17",      # Adults only
            "Unrated"     # No rating
        ]

        self.age_rating_dropdown = ctk.CTkComboBox(
            self.details_frame,
            values=age_rating_options,
            state="readonly",  # Make it read-only to limit input to the predefined options
            fg_color='#323740'
        )

        # Set the current value based on the film data (index 5 assumed to be the age rating)
        current_rating = self.film[5] if self.film[5] in age_rating_options else "Unrated"
        self.age_rating_dropdown.set(current_rating)

        self.age_rating_dropdown.grid(row=0, column=3, padx=10, pady=2, sticky="ew")


        # Film genre
        self.genre_label = ctk.CTkLabel(self.details_frame, text='Genre:', width=80)
        self.genre_label.grid(row=0, column=0, padx=10, pady=2, sticky="ew")
        self.genre_textbox = ctk.CTkTextbox(self.details_frame, height=10, width=200, fg_color='#323740', activate_scrollbars=False)
        self.genre_textbox.insert("0.0", self.film[3])  # Assuming genre is at index 3
        self.genre_textbox.grid(row=0, column=1, padx=10, pady=2, sticky="ew")

        # Film actors
        self.actors_label = ctk.CTkLabel(self.details_frame, text='Actors:', width=60)
        self.actors_label.grid(row=0, column=4, padx=10, pady=2, sticky="ew")
        self.actors_textbox = ctk.CTkTextbox(self.details_frame, height=10, width=400, fg_color='#323740', activate_scrollbars=False)
        self.actors_textbox.insert("0.0", self.film[4])  # Assuming actors are at index 4
        self.actors_textbox.grid(row=0, column=5, padx=10, pady=2, sticky="ew")

        # Film description
        self.film_description_textbox = ctk.CTkTextbox(self, wrap="char", height=100, fg_color='#323740')
        self.film_description_textbox.insert("0.0", self.film[2])  # Assuming description is at index 2
        self.film_description_textbox.grid(row=2, column=1, sticky='ew', pady=10, padx=10)

        # Editable fields
        self.editable_fields = [
            self.button_film_image,
            self.film_title_textbox,
            self.film_description_textbox,
            self.age_rating_dropdown,
            self.genre_textbox,
            self.actors_textbox,
        ]

    def init_buttons(self):
        """Initialize buttons for Save, Edit, and Back."""
        self.button_frame = ctk.CTkFrame(self, fg_color='#282c33')
        self.button_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.save_button = ctk.CTkButton(self.button_frame, text="Save", command=self.save_film)
        self.save_button.pack(side="right", padx=5)

        self.edit_button = ctk.CTkButton(self.button_frame, text="Edit", command=self.enter_edit_mode)
        self.edit_button.pack(side="right", padx=5)

        self.back_button = ctk.CTkButton(self.button_frame, text="Back", command=self.back)
        self.back_button.pack(side="left", padx=5)

    def clear_elements(self):
        """Clear all existing elements to avoid duplicates."""
        for widget in self.winfo_children():
            widget.destroy()

    def enable_edit(self):
        """Enable editing for all editable fields."""
        for field in self.editable_fields:
            field.configure(state='normal')
        self.save_button.configure(state="normal")

    def disable_edit(self):
        """Disable editing for all editable fields."""
        for field in self.editable_fields:
            field.configure(state='disabled')
        self.save_button.configure(state="disabled")

    def save_film(self):
        """Save changes to the film (add or update)."""
        try:
            title = self.film_title_textbox.get("0.0", "end").strip()
            genre = self.genre_textbox.get("0.0", "end").strip()
            description = self.film_description_textbox.get("0.0", "end").strip()
            actors = self.actors_textbox.get("0.0", "end").strip()
            rating = self.age_rating_textbox.get("0.0", "end").strip()

            if not title or not genre or not description or not actors or not rating:
                print("Error: All fields must be filled!")
                return

            # Check if an image was selected
            image_blob = getattr(self, "image_blob", None)

            if self.mode == "add_new":
                film_id = self.master.controller.add_new_film(
                    title=title, description=description, poster=image_blob,
                    genre=genre, actors=actors, age_rating=rating
                )
                print("Film added successfully!")
                self.mode = "view"
                self.film = self.master.controller.fetch_film_by_id(film_id)
            elif self.mode == "edit":
                self.master.controller.update_film(
                    film_id=self.film[0], title=title, description=description,
                    poster=image_blob, genre=genre, actors=actors, age_rating=rating
                )
                print("Film updated successfully!")
                self.mode = "view"

            self.disable_edit()
            self.update_mode()
        except Exception as e:
            print(f"Error saving film: {e}")


    def enter_edit_mode(self):
        """Switch to edit mode."""
        self.mode = "edit"
        self.update_mode()

    def back(self):
        """Handle the Back button behavior."""
        if self.mode == "edit":
            self.film = list(self.original_film_data)  # Restore original data
            self.mode = "view"
            self.init_frame_elements()
            self.init_buttons()
            self.update_mode()
        else:
            self.master.show_film_table_view()

    def update_mode(self):
        """Update UI elements based on the current mode."""
        if self.mode == "view":
            self.disable_edit()
            self.edit_button.configure(state="normal")
            self.save_button.configure(state="disabled")
        elif self.mode == "add_new" or self.mode == "edit":
            self.enable_edit()
            self.edit_button.configure(state="disabled")
            self.save_button.configure(state="normal")



    def select_image(self):
        """Handle selecting and processing a film image."""
        try:
            # Open file dialog to select the image
            image_path = ctk.filedialog.askopenfilename(
                title="Select an Image", filetypes=[('Image files', '*.png *.jpg *.jpeg')]
            )
            if not image_path:
                print("No image selected.")
                return

            # Load the image
            self.imagefile = Image.open(image_path)
            original_size = self.imagefile.size
            print(f"Original image size: {original_size}")

            # Define the target size as 150x200 (3:4 aspect ratio)
            target_width = 150
            target_height = 200

            # Resize the image to the target size while maintaining the aspect ratio
            self.imagefile = ImageOps.fit(
                self.imagefile, (target_width, target_height), method=Image.Resampling.LANCZOS
            )
            resized_size = self.imagefile.size
            print(f"Resized image size: {resized_size}")

            # Convert the image to a blob (binary data)
            image_blob = io.BytesIO()
            self.imagefile.save(image_blob, format="JPEG")  # Convert to a common format (e.g., JPEG)
            image_blob = image_blob.getvalue()

            # Save the blob in a variable to send to the controller
            self.image_blob = image_blob
            print("Image resized to 150x200 pixels and converted to blob.")

            # Display the image in the button (optional, for visualization)
            self.show_image_on_button()

            # Update the button states
            self.button_film_image.configure(fg_color='#a85f00', hover_color='#664822', state="normal")
        except Exception as e:
            print(f"Error processing image: {e}")



    def show_image_on_button(self):
        """Display the resized image on the button."""
        try:
            # Create a PhotoImage from the resized PIL image
            photo = ImageTk.PhotoImage(self.imagefile)

            # Set the image as the button background
            self.button_film_image.configure(image=photo)
            self.button_film_image.image = photo  # Keep a reference to prevent garbage collection
        except Exception as e:
            print(f"Error displaying image on button: {e}")



class FilmFrame(ctk.CTkFrame):
    def __init__(self, 
                 master, 
                 film_id,
                 ):
        
        super().__init__(master)
        self.controller = FilmController()
        self.configure(fg_color='#202329')

        # Configure the layout of the frame
        self.columnconfigure(0, weight=0)  # Column 0 (image button) has no resizing
        self.columnconfigure(1, weight=4)  # Column 1 (textboxes) takes more space
        self.rowconfigure((0), weight=0)  # Row 0 has no resizing
        self.rowconfigure((1), weight=1)  # Row 1 (film description) resizes with the window

        self.film = self.controller.fetch_film_by_id(film_id=film_id)
        print(self.film)

        self.title = self.film[1]
        self.poster = self.film[6]
        self.age_rating = self.film[5]
        self.genre = self.film[3]
        self.actors = self.film[4]
        self.description = self.film[2]

        self.init_frame_elements()
        self.load_frame_elements()

    def init_frame_elements(self):
        # Column 1: Button for adding a film image (disabled, placeholder for now)
        if self.film[6]:  # Assuming self.film[5] contains the blob data
            # Convert the blob data to an image
            image_blob = io.BytesIO(self.film[5])
            loaded_image = Image.open(image_blob)
            # Resize the image to fit the button (150x200)
            resized_image = ImageOps.fit(loaded_image, (150, 200), method=Image.Resampling.LANCZOS)
            # Convert to PhotoImage for CTkButton
            photo_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(150, 200))

            self.button_film_image = ctk.CTkButton(
                self,
                text='',  # No text if the image is displayed
                command=self.select_img,
                image=photo_image,
                height=200, width=150,
                fg_color='#282c33',
                hover_color='#323740'
            )
        else:
            # Default button when no image is available
            self.button_film_image = ctk.CTkButton(
                self,
                text='+Add Image',
                command=self.select_img,
                height=200, width=150,
                fg_color='#282c33',
                hover_color='#323740'
            )
        # Column 2: Textbox for film title (disabled by default)
        self.details_frame = ctk.CTkFrame(self, fg_color='#282c33')
        self.details_frame.rowconfigure((0,1), weight=1)
        self.details_frame.columnconfigure((0,1,2,3,4,5), weight=1)

        self.film_title_textbox = ctk.CTkTextbox(self.details_frame, wrap="char", height=40, fg_color='#323740',)
        self.film_title_textbox.insert("0.0", self.title)  # Insert the film title
        self.film_title_textbox.configure(state='disabled')  # Disable editing by default

        self.age_rating_label = ctk.CTkLabel(self.details_frame, text='Rating:', width=60)
        self.age_rating_textbox = ctk.CTkTextbox(self.details_frame, height=10, width=80, fg_color='#323740', activate_scrollbars=False)
        self.age_rating_textbox.insert("0.0", self.genre, "center")
        self.age_rating_textbox.configure(state='disabled') 
        self.genre_label = ctk.CTkLabel(self.details_frame, text='Genre:', width=80)
        self.genre_textbox = ctk.CTkTextbox(self.details_frame, height=10, width=200, fg_color='#323740', activate_scrollbars=False)
        self.genre_textbox.insert("0.0", self.genre, "center")
        self.genre_textbox.configure(state='disabled') 
        self.actors_label = ctk.CTkLabel(self.details_frame, text='Actors:', width=60)
        self.actors_textbox = ctk.CTkTextbox(self.details_frame, height=10, width=400, fg_color='#323740', activate_scrollbars=False)
        self.actors_textbox.insert("0.0", self.actors, "center")
        self.actors_textbox.configure(state='disabled') 

        # Textbox for film description (disabled by default)
        self.film_description_textbox = ctk.CTkTextbox(self, wrap="char", height=100, fg_color='#282c33',)
        self.film_description_textbox.insert("0.0", self.description)  # Insert the film description
        self.film_description_textbox.configure(state='disabled')  # Disable editing by default

    

    def load_frame_elements(self):
        # Layout the widgets on the grid
        self.button_film_image.grid(row=0, column=0, rowspan=2, sticky="nw", padx=5, pady=5, )  # Image button in column 0

        self.details_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)  # Title textbox in column 1

        self.film_title_textbox.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=5, pady=5)  # Title textbox in column 1

        self.age_rating_label.grid(row=1, column=0, padx=10, pady=2, sticky="ew")
        self.age_rating_textbox.grid(row=1, column=1, padx=0, pady=2, sticky="ew")
        self.genre_label.grid(row=1, column=2, padx=5, pady=2, sticky="ew")
        self.genre_textbox.grid(row=1, column=3, padx=2, pady=2, sticky="ew")
        self.actors_label.grid(row=1, column=4, padx=5, pady=2, sticky="ew")
        self.actors_textbox.grid(row=1, column=5, padx=2, pady=2, sticky="ew")


        self.film_description_textbox.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)  # Description textbox in column 1

    def select_img(self):
        pass



if __name__ == "__main__":
    root = ctk.CTk()
    FilmView(master=root).pack(fill="both", expand=True)
    root.mainloop()
