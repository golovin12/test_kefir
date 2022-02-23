from .models import UserModel


class EmailAuthBackend():

    def authenticate(self, request, login=None, password=None):
        try:
            user = UserModel.objects.get(email=login)
            if user.check_password(password):
                return user
            return None
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class LoginAuthBackend():

    def authenticate(self, request, login=None, password=None):
        try:
            user = UserModel.objects.get(login=login)
            if user.check_password(password):
                return user
            return None
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
