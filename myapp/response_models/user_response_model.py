
class UserResponse:
    """
    Class that represents a user response from the db
    """
    def __init__(self, id: int, email: str,role: str):
        """
        Constructor method for creating an instance of the class
        with the given id and email
        :param id: user's id
        :param email: user's email
        """
        self.id: int = id
        self.email: str = email
        self.role: str = role

    def __str__(self):
        return f"User's email: {self.email}"
