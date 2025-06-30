from models.film_model import FilmModel

class FilmController:
    def __init__(self):
        # Initialize the FilmModel instance
        self.model = FilmModel()

    def fetch_all_films(self, search=None, limit=10, offset=0):
        """
        Fetch films with optional search and pagination.

        Parameters:
        - search (str): Optional search term to filter films by title or genre.
        - limit (int): Maximum number of films to fetch.
        - offset (int): Offset for pagination.

        Returns:
        - list: A list of films matching the search and pagination criteria.
        """
        return self.model.get_all_films(search, limit, offset)

    def fetch_film_by_id(self, film_id):
        """
        Fetch a single film by its ID.

        Parameters:
        - film_id (int): The ID of the film to fetch.

        Returns:
        - tuple: A film record, or None if the film does not exist.
        """
        print(f"Fetch_film_by_id called for {film_id}, type: {type(film_id)}")


        return self.model.get_film_by_id(film_id)

    def add_new_film(self, title, description, poster, genre, actors, age_rating,):
        """
        Add a new film to the database.

        Parameters:
        - title (str): The title of the film.
        - description (str): The description of the film.
        - poster (str): The path to the film's poster image.
        - genre (str): The genre of the film.
        - actors (str): A comma-separated list of actors in the film.
        - age_rating (str): The age rating of the film.

        Returns:
        - None
        """
        self.model.add_film(title, description, poster, genre, actors, age_rating)

    def update_film(self, film_id, title=None, description=None, poster=None, genre=None, actors=None, age_rating=None):
        """
        Update an existing film's details in the database.

        Parameters:
        - film_id (int): The ID of the film to update.
        - title (str): Optional new title.
        - description (str): Optional new description.
        - poster (str): Optional new poster path.
        - genre (str): Optional new genre.
        - actors (str): Optional new actors.
        - age_rating (str): Optional new age rating.

        Returns:
        - None
        """
        self.model.update_film(film_id, title, description, poster, genre, actors, age_rating)

    def delete_film(self, film_id):
        """
        Delete a film from the database by its ID.

        Parameters:
        - film_id (int): The ID of the film to delete.

        Returns:
        - None
        """
        print(f"Delete_film called for {film_id}, type: {type(film_id)}")
        self.model.delete_film(film_id)
