from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned

UserModel = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Support authentication using either username or email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs) -> UserModel | None:

        if not username:
            return None

        def try_with(field):
            try:
                return UserModel.objects.get(**{field: username})
            except (UserModel.DoesNotExist, MultipleObjectsReturned):
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user (#20760).
                UserModel().set_password(password)

        user = (try_with("email") if username.count("@") == 1 else None) or try_with("username")

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
