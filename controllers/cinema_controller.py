from models.cinema_model import CinemaModel

class CinemaController:
    def __init__(self):
        # Initialize the CinemaModel instance
        self.model = CinemaModel()

    def fetch_all_cinemas(self):
        """
        Fetch all cinemas.

        Returns:
        - list: A list of all cinemas.
        """
        return self.model.get_all_cinemas()

    def fetch_cinema_by_id(self, cinema_id):
        """
        Fetch a cinema by its ID.

        Parameters:
        - cinema_id (int): The ID of the cinema.

        Returns:
        - tuple: Details of the cinema, or None if not found.
        """
        return self.model.get_cinema_by_id(cinema_id)

    def fetch_screens_by_cinema(self, cinema_id):
        """
        Fetch all screens for a specific cinema.

        Parameters:
        - cinema_id (int): The ID of the cinema.

        Returns:
        - list: A list of screens for the given cinema.
        """
        return self.model.get_screens_by_cinema(cinema_id)
    
    def fetch_screen_by_id(self, screen_id):
        return self.model.get_screen_by_id(screen_id)
    
    def add_cinema(self, address, screens):
        try:
            self.model.add_cinema(address, screens)
            print("Cinema added successfully!")
        except Exception as e:
            print(f"Error adding cinema: {e}")

        
