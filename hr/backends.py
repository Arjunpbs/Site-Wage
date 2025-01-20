from django.contrib.auth.backends import ModelBackend
from .models import HRUser
from employee.models import Employee

class HRUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = HRUser.objects.get(hrusername=username)
            if user.check_password(password):
                return user
        except HRUser.DoesNotExist:
            return None


