from models.showtime_model import ShowtimeModel

class ShowtimeController:
    def __init__(self):
        # Initialize the ShowtimeModel instance
        self.model = ShowtimeModel()

    def fetch_showtimes(self, search=None, limit=10, offset=0):
        """
        Fetch showtimes with optional search and pagination.

        Parameters:
        - search (str): Optional search term to filter by cinema name or film title.
        - limit (int): Maximum number of showtimes to fetch.
        - offset (int): Offset for pagination.

        Returns:
        - list: A list of showtimes matching the search and pagination criteria.
        """
        try:
            return self.model.get_all_showtimes(search, limit, offset)
        except Exception as e:
            print(f"Error fetching showtimes: {e}")
            return []

    def fetch_showtime_by_id(self, showtime_id):
        """
        Fetch a single showtime by its ID.

        Parameters:
        - showtime_id (int): The ID of the showtime to fetch.

        Returns:
        - tuple: A showtime record, or None if the showtime does not exist.
        """
        try:
            print(f"Fetch_showtime_by_id called for {showtime_id}, type: {type(showtime_id)}")
            return self.model.get_showtime_by_id(showtime_id)
        except Exception as e:
            print(f"Error fetching showtime by ID: {e}")
            return None

    def add_showtime(self, film_id, screen_id, date, time, price_lower, price_upper, vip_price):
        """
        Add a new showtime to the database.

        Parameters:
        - film_id (int): The ID of the film.
        - screen_id (int): The ID of the screen.
        - date (str): The date of the showtime (YYYY-MM-DD).
        - time (str): The time of the showtime (HH:MM:SS).
        - price_lower (float): The lower price for the showtime.
        - price_upper (float): The upper price for the showtime.
        - vip_price (float): The VIP price for the showtime.

        Returns:
        - None
        """
        try:
            self.model.add_showtime(film_id, screen_id, date, time, price_lower, price_upper, vip_price)
            print("Showtime added successfully!")
        except Exception as e:
            print(f"Error adding showtime: {e}")

    def update_showtime(self, showtime_id, film_id=None, screen_id=None, date=None, time=None,
                        price_lower=None, price_upper=None, vip_price=None):
        """
        Update an existing showtime. Only updates non-None fields.

        Parameters:
        - showtime_id (int): The ID of the showtime to update.
        - film_id (int): Optional new film ID.
        - screen_id (int): Optional new screen ID.
        - date (str): Optional new date (YYYY-MM-DD).
        - time (str): Optional new time (HH:MM:SS).
        - price_lower (float): Optional new lower price.
        - price_upper (float): Optional new upper price.
        - vip_price (float): Optional new VIP price.

        Returns:
        - None
        """
        try:
            self.model.update_showtime(
                showtime_id, film_id, screen_id, date, time, price_lower, price_upper, vip_price
            )
            print("Showtime updated successfully!")
        except Exception as e:
            print(f"Error updating showtime: {e}")

    def delete_showtime(self, showtime_id):
        """
        Delete a showtime by its ID.

        Parameters:
        - showtime_id (int): The ID of the showtime to delete.

        Returns:
        - None
        """
        try:
            self.model.delete_showtime(showtime_id)
            print(f"Showtime with ID {showtime_id} deleted successfully!")
        except Exception as e:
            print(f"Error deleting showtime: {e}")


    def fetch_showtimes_count_by_film_id(self, film_id):
        return self.model.get_showtime_count_by_film_id(film_id)

