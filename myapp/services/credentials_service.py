import os
import base64
import hashlib
import re


class CredentialsService:
    """
     Class that allow to code/decode passwords into/from hashes
     for further processing with database and check email and password
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Method to hash a password
        :param password: str - password that was entered
        :return: str - hashed password
        """
        salt = os.urandom(16)

        # Hashing the password with using algorithm PBKDF-2
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        # Combine the salt and hash in the aim to encode the result in Base64
        # for ease of storage and transmission
        combined = salt + hashed_password

        # Converting result to the string
        return base64.b64encode(combined).decode('utf-8')

    @staticmethod
    def check_password(stored_password: str, password: str) -> bool:
        """
        Method to check a stored password
        :param stored_password: str - hashed password from database
        :param password: str - password that was entered without hashing
        :return: bool - if password matches stored password
        """
        # Decode a Base64 string back into bytes
        combined = base64.b64decode(stored_password.encode('utf-8'))

        # Extracting salt and hash from the combination
        salt = combined[:16]  # First 16 bits - salt
        stored_hashed_password = combined[16:]  # Other is hash

        # Hashing the entered password using the same salt
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        # Comparing hashes
        return hashed_password == stored_hashed_password

    @staticmethod
    def check_credentials(email: str, password: str) -> bool:
        """
            Method that checks credentials (password and email).
            :param email: str - player's email
            :param password: str - player's password
            :return: True if credentials are valid, else False
            """
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        # Minimum 8 signs at password
        password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*+=/-]{8,}$"

        if not re.match(email_pattern, email):
            return False

        if not re.match(password_pattern, password):
            return False

        # If all checking points are passed
        return True
