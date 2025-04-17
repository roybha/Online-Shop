from django.core.exceptions import ValidationError
from myapp.models import User
from myapp.response_models.user_response_model import UserResponse
from myapp.services.credentials_service import CredentialsService
from django.contrib.auth import login


class DbService:
    """
    Class that operates on the database
    """

    @staticmethod
    def sign_up(email: str, password: str):
        """
        Registration of a new user
        """
        try:
            # Checking credentials
            if not CredentialsService.check_credentials(email, password):
                raise ValidationError("Неправильна пошта або пароль")

            # Checking existence of such user
            if User.objects.filter(email=email).exists():
                raise ValidationError("Користувач з таким email вже існує.")

            # Creating of new user
            user = User.objects.create_user(
                email=email,
                password=password,
            )
            return user
        except Exception as e:
            return str(e)

    @staticmethod
    def sign_in(request, email: str, password: str):
        """
        Entering into account with an email and a password
        """
        try:
            # Searching user via  the email
            user = User.objects.get(email=email)

            # Checking of the password
            if CredentialsService.check_password(user.password, password):
                # If the password is correct -> allow to enter and return
                login(request, user)
                return UserResponse(user.id, user.email)
            else:
                # Else -> don't allow to enter and return None
                return None
        except User.DoesNotExist:
            # If user with such email doesn't exist -> return None
            return None
