import uuid
from django.contrib.auth.base_user import BaseUserManager
from myapp.services.credentials_service import CredentialsService


class UserManager(BaseUserManager):
    """
    Custom manager class for correct operations while authenticating users
    """
    def create_user(self, email: str, password: str, **extra_fields):
        """
        Method that creates and saves a new user if all credentials are correct
        :param email: user's email
        :param password: user's password
        :return:
        """

        # if email | password isn't specified raise ValueError
        if not email:
            raise ValueError('Пошта має бути вказана')
        elif not password:
            raise ValueError('Пароль має бути вказаний')

        # automatically set username
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = f'{email.split("@")[0]}_{uuid.uuid4().hex[:6]}'

        # set role by default
        role = extra_fields.get('role', 'user')

        # set user's email
        user = self.model(email=email, **extra_fields)

        # hash user's password in one way if role is  admin
        if role == 'admin':
            user.set_password(password)
        else:
            # if user's role isn't admin hash in another way
            user.password = CredentialsService.hash_password(password)

        # save user instance in DB
        user.save(using=self._db)

        # return saved user
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Method that creates and saves a new superuser (admin)
        :param email: entered email for admin
        :param password: entered password for admin
        :param extra_fields: dictionary that contains all additional fields
        :return: instance of the created superuser
        """

        # setting is_staff column as True
        extra_fields.setdefault('is_staff', True)

        # setting is_superuser column as True
        extra_fields.setdefault('is_superuser', True)

        # setting is_active column as True
        extra_fields.setdefault('is_active', True)

        # if we are creating superuser his role will be admin
        extra_fields.setdefault('role', 'admin')

        # raise ValueError if is_staff | is_superuser isn't True
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # return the result of create_user method
        return self.create_user(email, password, **extra_fields)
