import bcrypt
from models.base_model import BaseModel

class UserModel(BaseModel):
    def hash_password(self, password):
        """
        Hash a password using bcrypt.

        Parameters:
        - password (str): The plaintext password.

        Returns:
        - str: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, password, hashed_password):
        """
        Verify a password against its hashed version.

        Parameters:
        - password (str): The plaintext password.
        - hashed_password (str): The hashed password from the database.

        Returns:
        - bool: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def create_user(self, username, password, role):
        """
        Create a new user in the database with a hashed password.

        Parameters:
        - username (str): The username for the new user.
        - password (str): The plaintext password for the new user.
        - role (str): The role of the new user.

        Returns:
        - bool: True if the user is successfully created, False otherwise.
        """
        try:
            hashed_password = self.hash_password(password)
            query = "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)"
            self.cursor.execute(query, (username, hashed_password, role))
            self.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False

    def get_user_by_credentials(self, username, password):
        """
        Fetch a user from the database by username and password.

        Parameters:
        - username (str): The username entered by the user.
        - password (str): The plaintext password entered by the user.

        Returns:
        - tuple: The user record if authentication succeeds, None otherwise.
        """
        print(f"Debug: Attempting to authenticate user {username}")
        query = "SELECT id, username, password, role FROM Users WHERE username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result:
            user_id, username, hashed_password, role = result
            if self.verify_password(password, hashed_password):
                print(f"Debug: Authentication successful for user {username}")
                return user_id, username, role
            else:
                print("Debug: Password verification failed.")
        return None

    def get_all_users(self):
        query = "SELECT id, username, role FROM Users"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_user_by_id(self, user_id):
        """
        Fetch a user from the database by id.

        Parameters:
        - user_id (int): The ID of the user to update.

        Returns:
        - tuple: The user record if found, None otherwise.
        """
        print(f"Debug: Attempting to aquire user by user id: {user_id}")
        query = "SELECT username, role FROM Users WHERE id = ?"
        self.cursor.execute(query, (user_id))
        result = self.cursor.fetchone()
        return result

    def update_user_role(self, user_id, new_role):
        """
        Update the role of an existing user.

        Parameters:
        - user_id (int): The ID of the user to update.
        - new_role (str): The new role to assign to the user.

        Returns:
        - bool: True if the update was successful, False otherwise.
        """
        try:
            query = "UPDATE Users SET role = ? WHERE id = ?"
            self.cursor.execute(query, (new_role, user_id))
            self.commit()
            return True
        except Exception as e:
            print(f"Error updating user role: {e}")
            return False

    def delete_user(self, user_id):
        """
        Delete a user from the database.

        Parameters:
        - user_id (int): The ID of the user to delete.

        Returns:
        - bool: True if the deletion was successful, False otherwise.
        """
        try:
            query = "DELETE FROM Users WHERE id = ?"
            self.cursor.execute(query, (user_id,))
            self.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        
