from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using
    either their username or their email address (case-insensitive).
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if not username or not password:
            return None

        clean_identifier = username.strip()

        # 1. First attempt lookup by username (case-insensitive)
        user = UserModel.objects.filter(username__iexact=clean_identifier).first()

        # 2. If not found, attempt lookup by email (case-insensitive)
        if not user:
            user = UserModel.objects.filter(email__iexact=clean_identifier).first()

        # 3. Validate password and active status
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
