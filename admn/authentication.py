from django.contrib.auth.backends import ModelBackend
from .models import AdminInfo
from django.contrib.auth import get_user_model

class AdminBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, admn_id=None, admn_password=None):
        if admn_id is not None and admn_password is not None:
            try:
                admn = AdminInfo.objects.get(admn_id=admn_id)
                if admn.admn_password == admn_password:
                    return admn
            except AdminInfo.DoesNotExist:
                return None
        
        # If employee authentication fails or it's not an employee login attempt, fall back to default authentication backend
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Set last_login to None to skip the last_login field check
                if hasattr(user, 'last_login'):
                    user.last_login = None
                return user
        except User.DoesNotExist:
            return None
