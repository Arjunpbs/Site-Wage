from django.contrib.auth.backends import ModelBackend
from .models import HrInfo
from django.contrib.auth import get_user_model

class HrBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, hr_id=None, hr_password=None):
        if hr_id is not None and hr_password is not None:
            try:
                hr = HrInfo.objects.get(hr_id=hr_id)
                if hr.hr_password == hr_password:
                    return hr
            except HrInfo.DoesNotExist:
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
