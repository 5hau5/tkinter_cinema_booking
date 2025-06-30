from models.film_listing_model import FilmListingModel

class FilmListingController:
    def __init__(self):
        # Initialize the FilmModel instance
        self.model = FilmListingModel()

    def fetch_all_film_listings(self, cinema_id, datetime):
        return self.model.get_all_film_listings(cinema_id=cinema_id, datetime=datetime)