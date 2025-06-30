import customtkinter as ctk
from controllers.booking_controller import BookingController
from controllers.user_controller import UserController
from controllers.cinema_controller import CinemaController
from controllers.showtime_controller import ShowtimeController
from controllers.film_controller import FilmController
import calendar
import datetime
from tkinter.messagebox import showerror, showinfo
# staff report on who booked the most per month for a specific cinema

class CreateReportView(ctk.CTkFrame):
    def __init__(self, master, cinema_id):
        super().__init__(master)

        self.configure(fg_color='#282c33')
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1,2), weight=0)

        StaffReportView(self).grid(row=1, pady=10, padx=10)
        CinemaSaleReportView(self, cinema_id).grid(row=2, pady=10, padx=10)
        FilmSaleReportView(self).grid(row=3, pady=10, padx=10)

    def show_showtime_table_view(self):
        print("show_showtime_table_view called")


    def show_add_showtime(self):
        """Switch to the ShowtimeDetailView in add_new mode."""


    def switch_view(self, new_view):
        # Forget the current widgets and load the new view
        for widget in self.winfo_children():
            widget.forget()
        new_view.pack(expand=True, fill="both")


class StaffReportView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Initialize controllers

        self.user_controller = UserController()
        self.booking_controller = BookingController()

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Staff Booking Report")
        self.label.grid(row=0, column=0, pady=10, padx=10)

        self.configure(fg_color='#333842')
        self.month_combo()
        self.year_combo()

        self.create_report_button = ctk.CTkButton(self, text="Create Report", command=self.create_report)
        self.create_report_button.grid(row=3, column=0, pady=10, padx=10)

    def month_combo(self):
        # Combo box for all month names
        current_month = datetime.datetime.now().month
        self.month_dropdown = ctk.CTkComboBox(
            self,
            values=list(calendar.month_name[1:]),  # Skip the first empty item
        )
        self.month_dropdown.grid(row=1, column=0, padx=10)
        self.month_dropdown.set(calendar.month_name[current_month])

    def year_combo(self):
        # Combo box for years from 2020 to the current year
        current_year = datetime.datetime.now().year
        self.year_dropdown = ctk.CTkComboBox(
            self,
            values=[str(year) for year in range(2020, current_year + 1)],
        )
        self.year_dropdown.grid(row=2, column=0, padx=10)
        self.year_dropdown.set(str(current_year))

    def create_report(self):
        # Create a report file with users and their booking details for the selected month
        try:
            selected_month = self.month_dropdown.get()
            selected_year = self.year_dropdown.get()

            # Get numeric month
            month_number = list(calendar.month_name).index(selected_month)
            month_str = f"{selected_year}-{month_number:02}"  # Format as YYYY-MM

            users = self.user_controller.fetch_all_users()
            report_data = []

            for user in users:
                user_id, username, role = user
                print(user_id, username, role)

                # Fetch bookings for the user
                bookings = self.booking_controller.fetch_all_bookings_by_user_id(user_id, month_str)
                total_bookings = len(bookings)
                total_revenue = sum(float(booking["total_cost"]) for booking in bookings)

                if total_bookings > 0:
                    report_data.append((user_id, username, total_bookings, total_revenue))

            # Sort by the number of bookings in descending order
            report_data.sort(key=lambda x: x[2], reverse=True)

            # Create report file
            report_filename = f"staff_booking_report_{selected_year}_{month_number:02}.txt"
            with open(report_filename, "w") as file:
                file.write(f"Staff Booking Report for {selected_month} {selected_year}\n")
                file.write("=" * 50 + "\n")
                file.write(f"{'User ID':<10} {'Username':<20} {'Bookings':<10} {'Revenue':<10}\n")
                file.write("-" * 50 + "\n")
                for user_id, username, bookings, revenue in report_data:
                    file.write(f"{user_id:<10} {username:<20} {bookings:<10} ${revenue:<10.2f}\n")

            showinfo("Report Created", f"Report created successfully: {report_filename}")

        except Exception as e:
            showerror("Error", f"An error occurred while creating the report: {str(e)}")
        


class CinemaSaleReportView(ctk.CTkFrame):
    def __init__(self, master, cinema):
        super().__init__(master)
        self.master = master
        self.configure(fg_color='#333842')
        self.cinema_controller = CinemaController()
        self.booking_controller = BookingController()
        self.cinema_id = cinema

        # Title
        self.title_label = ctk.CTkLabel(self, text="Cinema Sales Report")
        self.title_label.grid(row=0, column=0, pady=10, padx=10)



        self.cinema_combo()

        # Generate Report Button
        self.generate_report_button = ctk.CTkButton(self, text="Generate Report", command=self.create_report)
        self.generate_report_button.grid(row=2, column=0, pady=10, padx=10)

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
        self.cinema_dropdown.grid(row=1, column=0, padx=10, pady=10)

        if self.cinemas:
            first_cinema = list(self.cinema_name_to_id.keys())[0]
            self.cinema_dropdown.set(first_cinema)
            self.cinema_id = self.cinema_name_to_id[first_cinema]

    def update_selected_cinema_id(self, selected_cinema_name):
        self.cinema_id = self.cinema_name_to_id.get(selected_cinema_name)

    def create_report(self):
        if not self.cinema_id:
            showerror("Error", "Please select a cinema.")
            return

        try:
            # Fetch all bookings for the selected cinema
            bookings = self.booking_controller.fetch_all_bookings(cinema_id=self.cinema_id)

            # Initialize report data
            total_bookings = len(bookings)
            total_revenue = sum(float(booking["total_cost"]) for booking in bookings)
            unique_films = set(booking["film_name"] for booking in bookings)
            unique_shows = set(booking["showtime_id"] for booking in bookings)

            # Prepare report details
            report_filename = f"cinema_sales_report_{self.cinema_id}.txt"
            with open(report_filename, "w") as file:
                file.write(f"Cinema Sales Report\n")
                file.write("=" * 50 + "\n")
                file.write(f"Cinema ID: {self.cinema_id}\n")
                file.write(f"Total Bookings: {total_bookings}\n")
                file.write(f"Unique Films Shown: {len(unique_films)}\n")
                file.write(f"Unique Shows: {len(unique_shows)}\n")
                file.write(f"Total Revenue: ${total_revenue:.2f}\n")
                file.write("=" * 50 + "\n")
                file.write(f"\nDetailed Bookings:\n")
                for booking in bookings:
                    file.write(f"- Booking Ref: {booking['booking_ref']}, Film: {booking['film_name']}, Cost: ${booking['total_cost']}\n")

            showinfo("Report Created", f"Report successfully created: {report_filename}")

        except Exception as e:
            print("Error", f"An error occurred while generating the report: {str(e)}")

class FilmSaleReportView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.configure(fg_color='#333842')
        
        self.booking_controller = BookingController()
        self.showtime_controller = ShowtimeController()

        # Title
        self.title_label = ctk.CTkLabel(self, text="Film Sales Report")
        self.title_label.grid(row=0, column=0, pady=10, padx=10)

        # Generate Report Button
        self.generate_report_button = ctk.CTkButton(self, text="Generate Report", command=self.create_report)
        self.generate_report_button.grid(row=1, column=0, pady=10, padx=10)

    def create_report(self):
        """
        Generate a sales report for all films, sorted by film IDs.
        """
        try:
            # Fetch all films
            films = FilmController().fetch_all_films()
            if not films:
                raise ValueError("No films found in the database.")

            # Prepare report filename
            report_filename = "film_sales_report.txt"

            # Open the file for writing
            with open(report_filename, "w") as file:
                file.write("Film Sales Report\n")
                file.write("=" * 50 + "\n")

                # Iterate through each film and generate the report
                for film in sorted(films, key=lambda x: x[0]):  # Sort by film ID
                    film_id, film_name = film[0], film[1]

                    # Fetch the number of showtimes for the film
                    showtime_count = self.showtime_controller.fetch_showtimes_count_by_film_id(film_id)

                    # Fetch all bookings for the film
                    bookings = self.booking_controller.fetch_all_bookings_by_film_id(film_id)

                    # Calculate total bookings and revenue
                    total_bookings = len(bookings)
                    total_revenue = sum(float(booking["total_cost"]) for booking in bookings)

                    # Write the film's report to the file
                    file.write(f"Film ID: {film_id}\n")
                    file.write(f"Film Name: {film_name}\n")
                    file.write(f"Total Showtimes: {showtime_count}\n")
                    file.write(f"Total Bookings: {total_bookings}\n")
                    file.write(f"Total Revenue: ${total_revenue:.2f}\n")
                    file.write("-" * 50 + "\n")

            # Inform the user that the report was successfully created
            showinfo("Report Created", f"Report successfully created: {report_filename}")

        except Exception as e:
            showerror("Error", f"An error occurred while generating the report: {str(e)}")
