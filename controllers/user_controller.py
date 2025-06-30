from models.user_model import UserModel

class UserController:
    def __init__(self):
        self.model = UserModel()

    def authenticate(self, username, password):
        """
        Authenticate the user by checking credentials in the database.

        Parameters:
        - username (str): The username entered by the user.
        - password (str): The password entered by the user.

        Returns:
        - dict: The user data if authentication succeeds, None otherwise.
        """
        user = self.model.get_user_by_credentials(username, password)
        return user

    def add_user(self, username, password, role):
        self.model.create_user(username, password, role)

    def update_user_role(self, user_id, new_role):
        self.model.update_user_role(user_id, new_role)

    def delete_user(self, user_id):
        self.model.delete_user(user_id)

    def get_user_details(self, user_id):
        """
        Retrieve details of a specific user.

        Parameters:
        - user_id (int): The ID of the user to retrieve details for.

        Returns:
        - dict: User details if the user exists, None otherwise.
        """
        return self.model.get_user_by_id(user_id)

    def fetch_all_users(self):
        return self.model.get_all_users()