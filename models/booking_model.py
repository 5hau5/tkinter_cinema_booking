from .base_model import BaseModel
import re

class BookingModel(BaseModel):
    def get_all_bookings(self, cinema_id, date=None):
        """
        Fetches all bookings with a required cinema ID and optional booking date.

        Args:
            cinema_id (int): The ID of the cinema to filter by.
            date (str, optional): The booking date to filter by (format: YYYY-MM-DD).

        Returns:
            list: A list of dictionaries, each containing detailed booking information.
        """
        try:
            if not cinema_id:
                raise ValueError("cinema_id is required")

            query = """
                SELECT 
                    b.id AS booking_id,
                    b.booking_ref AS booking_reference,
                    b.user_id AS user_id,
                    u.username AS username,
                    b.showtime_id AS showtime_id,
                    st.film_id AS film_id,
                    f.title AS film_name,
                    c1.name AS cinema_name_screen,
                    s.screen_number AS screen_number,
                    b.seats AS seats,
                    b.total_cost AS total_cost,
                    b.booking_date AS booking_date,
                    b.booking_time AS booking_time,
                    c2.name AS cinema_name_booking
                FROM bookings b
                LEFT JOIN users u ON b.user_id = u.id
                LEFT JOIN showtimes st ON b.showtime_id = st.id
                LEFT JOIN films f ON st.film_id = f.id
                LEFT JOIN screens s ON st.screen_id = s.id
                LEFT JOIN cinemas c1 ON s.cinema_id = c1.id
                LEFT JOIN cinemas c2 ON b.cinema_id = c2.id
                WHERE b.cinema_id = ?
            """
            params = [cinema_id]

            if date:
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                    raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")
                query += " AND b.booking_date = ?"
                params.append(date)

            print("Query:", query)
            print("Params:", params)

            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            if not rows:
                print(f"No bookings found for cinema_id={cinema_id}, date={date}")

            keys = [
                "booking_id",
                "booking_ref",
                "user_id",
                "username",
                "showtime_id",
                "film_id",
                "film_name",
                "cinema_name",
                "screen_number",
                "booked_seats",
                "total_cost",
                "booking_date",
                "booking_time",
                "booked_by_cinema"
            ]
            bookings = [dict(zip(keys, row)) for row in rows]

            return bookings

        except Exception as e:
            print(f"Error fetching bookings: {e}")
            return []

            


    def create_booking(self, booking_ref, user_id, showtime_id, seats, total_cost, date, time, cinema_id):
        try:
            # Step 2: Insert the booking into the database
            query = """
                INSERT INTO bookings (booking_ref, user_id, showtime_id, seats, total_cost, booking_date, booking_time, cinema_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (booking_ref, user_id, showtime_id, seats, total_cost, date, time, cinema_id))
            self.commit()

            return True
        except Exception as e:
            print(f"Error creating booking: {e}")
            return False


    def count_bookings(self, showtime_id):
        # Count existing bookings for the given showtime
        query_count = "SELECT COUNT(*) FROM bookings WHERE showtime_id = ?"
        self.cursor.execute(query_count, (showtime_id,))
        booking_count = self.cursor.fetchone()[0]  
        return booking_count



    def get_all_available_seats(self, showtime_id):
        """
        Returns the available seats for a given showtime by identifying booked seats
        and determining the remaining seats for each type.

        Args:
            showtime_id (int): The ID of the showtime for which to calculate available seats.

        Returns:
            dict: A dictionary with keys 'vip', 'upper_hall', 'lower_hall' and their respective available seat numbers.
        """
        # Step 1: Fetch screen capacities
        query_screen = """
            SELECT lower_hall_capacity, upper_hall_capacity, vip_seats
            FROM screens
            WHERE id = (SELECT screen_id FROM showtimes WHERE id = ?)
        """
        self.cursor.execute(query_screen, (showtime_id,))
        screen_data = self.cursor.fetchone()
        print(f"Screen data: {screen_data}")

        if not screen_data:
            raise ValueError(f"No screen data found for showtime ID {showtime_id}")

        lower_hall_capacity, upper_hall_capacity, vip_capacity = screen_data

        # Step 2: Fetch booked seats
        query_booked = """
            SELECT seats
            FROM bookings
            WHERE showtime_id = ?
        """
        self.cursor.execute(query_booked, (showtime_id,))
        booked_data = self.cursor.fetchall()
        print(f"Booked data: {booked_data}")

        # Combine all booked seats into a set
        booked_seats = set()
        if booked_data:
            for row in booked_data:
                # Split the `seats` string and add to the set
                booked_seats.update(map(int, row[0].split(',')))  # Assumes seats are stored as comma-separated strings

        print(f"Booked seats: {booked_seats}")

        # Step 3: Generate all possible seat numbers for each type
        vip_seats = set(range(1, vip_capacity + 1))
        upper_hall_seats = set(range(vip_capacity + 1, vip_capacity + upper_hall_capacity + 1))
        lower_hall_seats = set(range(vip_capacity + upper_hall_capacity + 1, vip_capacity + upper_hall_capacity + lower_hall_capacity + 1))

        # Step 4: Subtract booked seats from total seats
        available_seats = {
            'vip': sorted(vip_seats - booked_seats),
            'upper_hall': sorted(upper_hall_seats - booked_seats),
            'lower_hall': sorted(lower_hall_seats - booked_seats),
        }

        print(f"Available seats: {available_seats}")
        return available_seats
    
    def cancel_booking(self, booking_id):
        query = "DELETE FROM Bookings WHERE id = ?"
        self.cursor.execute(query, (booking_id,))
        self.commit()


    def get_all_bookings_by_user_id(self, user_id, month=None):
        """
        Fetches all bookings for a given user and optional month.

        Args:
            user_id (int): The ID of the user to filter by.
            month (str, optional): The booking month to filter by (format: YYYY-MM).

        Returns:
            list: A list of dictionaries containing booking_id and total_cost.
        """
        try:
            if not user_id:
                raise ValueError("user_id is required")

            # Base query
            query = """
                SELECT 
                    b.id AS booking_id,
                    b.total_cost AS total_cost
                FROM bookings b
                WHERE b.user_id = ?
            """
            params = [user_id]

            # Add filter for month if provided
            if month:
                if not re.match(r"^\d{4}-\d{2}$", month):
                    raise ValueError("Invalid month format. Expected format: YYYY-MM")
                query += " AND strftime('%Y-%m', b.booking_date) = ?"
                params.append(month)

            print("Query:", query)
            print("Params:", params)

            # Execute query
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()

            if not rows:
                print(f"No bookings found for user_id={user_id}, month={month}")

            # Format the result as a list of dictionaries
            bookings = [{"booking_id": row[0], "total_cost": float(row[1])} for row in rows]

            return bookings

        except Exception as e:
            print(f"Error fetching bookings: {e}")
            return []


    def get_all_bookings_by_film_id(self, film_id):
        """
        Fetch all bookings for a specific film with only booking_id and total_cost.

        Args:
            film_id (int): The ID of the film.

        Returns:
            list: A list of dictionaries containing booking_id and total_cost for each booking.
        """
        try:
            query = """
                SELECT 
                    b.id AS booking_id,
                    b.total_cost AS total_cost
                FROM bookings b
                JOIN showtimes st ON b.showtime_id = st.id
                WHERE st.film_id = ?
            """
            self.cursor.execute(query, (film_id,))
            rows = self.cursor.fetchall()

            # Format the result as a list of dictionaries
            bookings = [{"booking_id": row[0], "total_cost": float(row[1])} for row in rows]

            return bookings

        except Exception as e:
            print(f"Error fetching bookings for film_id={film_id}: {e}")
            return []
        
    def get_all_bookings_by_showtime_id(self, showtime_id):
        """
        Fetch all bookings for a specific showtime.

        Args:
            showtime_id (int): The ID of the showtime.

        Returns:
            a list of tuples of booking ids
        """
        try:
            query = """
                SELECT 
                    b.id AS booking_id
                FROM bookings b
                WHERE b.showtime_id = ?
            """
            self.cursor.execute(query, (showtime_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching bookings for showtime_id={showtime_id}: {e}")
            return []
