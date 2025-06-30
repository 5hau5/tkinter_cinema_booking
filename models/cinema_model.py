from .base_model import BaseModel


class CinemaModel(BaseModel):
    def get_all_cinemas(self):
        """
        Retrieve all cinemas from the database.

        Returns:
        - list: A list of tuples containing cinema details.
        """
        query = "SELECT id, name, location_city, address FROM Cinemas"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_cinema_by_id(self, cinema_id):
        """
        Retrieve a specific cinema by its ID.

        Parameters:
        - cinema_id (int): The ID of the cinema.

        Returns:
        - tuple: Details of the cinema, or None if not found.
        """
        query = "SELECT id, name, location_city, address FROM Cinemas WHERE id = ?"
        self.cursor.execute(query, (cinema_id,))
        return self.cursor.fetchone()

    
    def get_screen_by_id(self, screen_id):

        query = "SELECT id, screen_number FROM Screens WHERE id = ?"
        self.cursor.execute(query, (screen_id,))
        return self.cursor.fetchone()
    
    def add_cinema(self, address, screens):
        """
        Add a new cinema and its associated screens to the database.

        Args:
            address (str): The address of the cinema.
            screens (list): A list of dictionaries with screen details.
        """
        try:
            # Derive name and location from the address
            address_parts = address.split(", ")
            if len(address_parts) < 2:
                raise ValueError("Invalid address format. Ensure it includes a street and city.")

            city = address_parts[-1].strip()  # Last part is the city
            name = f"Horizon Cinema {city}"
            location = city

            # Insert cinema into cinemas table
            query_cinema = """
                INSERT INTO cinemas (name, location_city, address)
                VALUES (?, ?, ?)
            """
            self.cursor.execute(query_cinema, (name, location, address))
            self.commit()

            # Fetch the new cinema_id
            cinema_id = self.cursor.lastrowid

            # Insert screens into screens table
            query_screen = """
                INSERT INTO screens (cinema_id, screen_number, lower_hall_capacity, upper_hall_capacity, vip_seats)
                VALUES (?, ?, ?, ?, ?)
            """

            for i, screen in enumerate(screens, start=1):  # Screen numbers start from 1
                screen_number = f"Screen {i}"  # Save as "Screen 1", "Screen 2", etc.
                self.cursor.execute(query_screen, (
                    cinema_id,
                    screen_number,  # Use the formatted screen number
                    screen["lower_seats_cap"],
                    screen["upper_seats_cap"],
                    screen["vip_seats_cap"]
                ))

            self.commit()

            print(f"Cinema '{name}' with screens added successfully.")

        except Exception as e:
            print(f"Error adding cinema: {e}")



    def get_screens_by_cinema(self, cinema_id):
        """
        Fetches the screens for a given cinema.

        Args:
            cinema_id (int): The ID of the cinema.

        Returns:
            list: A list of tuples, where each tuple contains the screen ID and screen number.
        """
        try:
            query = "SELECT id, screen_number FROM Screens WHERE cinema_id = ?"
            self.cursor.execute(query, (cinema_id,))
            screens = self.cursor.fetchall()

            if not screens:
                print(f"No screens found for cinema ID: {cinema_id}")

            return screens
        except Exception as e:
            print(f"Error fetching screens for cinema ID {cinema_id}: {e}")
            return []

