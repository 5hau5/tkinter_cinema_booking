from .base_model import BaseModel

class FilmListingModel(BaseModel):
    def get_all_film_listings(self, cinema_id, datetime):
        """
        Retrieve all unique film listings for a specific cinema on a given datetime.

        Parameters:
        - cinema_id (int): The ID of the cinema.
        - datetime (datetime): The datetime for which to fetch film listings.

        Returns:
        - dict: A dictionary where keys are film IDs and values are lists of showtime IDs.
        """

        query = """
            SELECT DISTINCT s.film_id, s.id AS showtime_id
            FROM Showtimes s
            JOIN Screens sc ON s.screen_id = sc.id
            WHERE sc.cinema_id = ?
            AND s.date = ?  -- Restrict to the same date
            AND time(s.time) >= time(?)  -- Restrict to times greater than or equal to the specified time
        """

        self.cursor.execute(query, (cinema_id, datetime.strftime("%Y-%m-%d"), datetime.strftime("%H:%M")))
        results = self.cursor.fetchall()  # Results will be a list of tuples (film_id, showtime_id)

        # Build the dictionary
        film_dict = {}
        for film_id, showtime_id in results:
            if film_id not in film_dict:
                film_dict[film_id] = []  # Initialize a list for this film ID
            film_dict[film_id].append(showtime_id)  # Append the showtime ID to the film's list

        return film_dict
