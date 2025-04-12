from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager class for correct operations while authenticating users
    """
    def create_user(self, email: str, password: str):
        """
        Method that creates and saves a new user if all credentials are correct
        :param email: user's email
        :param password: user's password
        :return:
        """
        if not email:
            raise ValueError('Пошта має бути вказана')
        elif not password:
            raise ValueError('Пароль має бути вказаний')

        user = self.model(email=email, password=password)
        user.save(using=self._db)
        return user
