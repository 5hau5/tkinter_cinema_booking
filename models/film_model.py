from .base_model import BaseModel

class FilmModel(BaseModel):
    def get_all_films(self, search=None, limit=10, offset=0):
        """
        Fetch films from the database with optional search and pagination.

        Parameters:
        - search (str): Optional search term to filter films by title or genre.
        - limit (int): Maximum number of films to fetch.
        - offset (int): Offset for pagination.

        Returns:
        - list: A list of tuples representing the films.
        """
        query = "SELECT id, title, description, poster, genre, actors, age_rating FROM Films"
        params = []

        if search:
            query += " WHERE title LIKE ? OR genre LIKE ?"
            params.extend([f"%{search}%", f"%{search}%"])

        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_film_by_id(self, film_id):
        """
        Fetch a single film by its ID.
        
        Parameters:
        - film_id (int): The ID of the film to fetch.
        
        Returns:
        - tuple: A tuple representing the film, or None if not found.
        """

        print(f"get_film_bY_id called with {film_id}")
        query = "SELECT id, title, description, genre, actors, age_rating, poster FROM Films WHERE id = ?"
        self.cursor.execute(query, (film_id,))
        return self.cursor.fetchone()

    def add_film(self, title, description, poster, genre, actors, age_rating):
        """
        Add a new film to the database.
        
        Parameters:
        - title (str): The title of the film.
        - description (str): A description of the film.
        - poster:
        - genre (str): The genre of the film.
        - actors (str): A comma-separated list of actors in the film.
        - age_rating (str): The age rating of the film.
        
        Returns:
        - None
        """
        query = """
        INSERT INTO Films (title, description, poster, genre, actors, age_rating)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (title, description, poster, genre, actors, age_rating))
        self.commit()

    def update_film(self, film_id, title=None, description=None, poster=None, genre=None, actors=None, age_rating=None):
        """
        Update an existing film in the database. Only updates non-None fields.
        
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
        fields = []
        params = []
        
        if title:
            fields.append("title = ?")
            params.append(title)
        if description:
            fields.append("description = ?")
            params.append(description)
        if poster:
            fields.append("poster = ?")
            params.append(poster)
        if genre:
            fields.append("genre = ?")
            params.append(genre)
        if actors:
            fields.append("actors = ?")
            params.append(actors)
        if age_rating:
            fields.append("age_rating = ?")
            params.append(age_rating)
        
        params.append(film_id)
        query = f"UPDATE Films SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.commit()

    def delete_film(self, film_id):
        """
        Delete a film from the database by its ID.
        
        Parameters:
        - film_id (int): The ID of the film to delete.
        
        Returns:
        - None
        """
        query = "DELETE FROM Films WHERE id = ?"
        self.cursor.execute(query, (film_id,))
        self.commit()
