from .base_model import BaseModel

class ShowtimeModel(BaseModel):
    def get_all_showtimes(self, search=None, limit=10, offset=0):
        """
        Fetch all showtimes with optional search and pagination.

        Parameters:
        - search (str): Optional search term to filter by cinema name or film title.
        - limit (int): Maximum number of showtimes to fetch.
        - offset (int): Offset for pagination.

        Returns:
        - list: A list of tuples with showtime details.
        """
        query = """
        SELECT 
            s.id AS showtime_id,
            f.title AS film_name,
            sc.id AS screen_id,
            sc.screen_number,
            c.id AS cinema_id,
            c.name AS cinema_name,
            s.date,
            s.time,
            s.price_lower,
            s.price_upper,
            s.vip_price
        FROM Showtimes s
        JOIN Films f ON s.film_id = f.id
        JOIN Screens sc ON s.screen_id = sc.id
        JOIN Cinemas c ON sc.cinema_id = c.id
        """
        params = []

        if search:
            query += " WHERE c.name LIKE ? OR f.title LIKE ?"
            params.extend([f"%{search}%", f"%{search}%"])

        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_showtime_by_id(self, showtime_id):
        """
        Fetch a single showtime by its ID.

        Parameters:
        - showtime_id (int): The ID of the showtime to fetch.

        Returns:
        - tuple: A tuple with showtime details, or None if not found.
        """
        query = """
        SELECT 
            s.id AS showtime_id,
            f.title AS film_name,
            sc.id AS screen_id,
            sc.screen_number,
            c.id AS cinema_id,
            c.name AS cinema_name,
            s.date,
            s.time,
            s.price_lower,
            s.price_upper,
            s.vip_price
        FROM Showtimes s
        JOIN Films f ON s.film_id = f.id
        JOIN Screens sc ON s.screen_id = sc.id
        JOIN Cinemas c ON sc.cinema_id = c.id
        WHERE s.id = ?
        """
        self.cursor.execute(query, (showtime_id,))
        return self.cursor.fetchone()

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
        query = """
        INSERT INTO Showtimes (film_id, screen_id, date, time, price_lower, price_upper, vip_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (film_id, screen_id, date, time, price_lower, price_upper, vip_price))
        self.commit()

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
        fields = []
        params = []

        if film_id:
            fields.append("film_id = ?")
            params.append(film_id)
        if screen_id:
            fields.append("screen_id = ?")
            params.append(screen_id)
        if date:
            fields.append("date = ?")
            params.append(date)
        if time:
            fields.append("time = ?")
            params.append(time)
        if price_lower:
            fields.append("price_lower = ?")
            params.append(price_lower)
        if price_upper:
            fields.append("price_upper = ?")
            params.append(price_upper)
        if vip_price:
            fields.append("vip_price = ?")
            params.append(vip_price)

        params.append(showtime_id)
        query = f"UPDATE Showtimes SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.commit()

    def delete_showtime(self, showtime_id):
        """
        Delete a showtime by its ID.

        Parameters:
        - showtime_id (int): The ID of the showtime to delete.

        Returns:
        - None
        """
        query = "DELETE FROM Showtimes WHERE id = ?"
        self.cursor.execute(query, (showtime_id,))
        self.commit()

    def get_showtime_count_by_film_id(self, film_id):
        """
        Fetch the count of showtimes for a given film ID.

        Args:
            film_id (int): The ID of the film.

        Returns:
            int: The number of showtimes for the film.
        """
        query = """
        SELECT COUNT(s.id) AS showtime_count
        FROM showtimes s
        WHERE s.film_id = ?
        """
        try:
            self.cursor.execute(query, (film_id,))
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error fetching showtime count for film ID {film_id}: {e}")
            return 0
