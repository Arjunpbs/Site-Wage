from django.contrib.auth.backends import ModelBackend
from .models import EmployeeInfo
from django.contrib.auth import get_user_model

class EmployeeBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, emp_id=None, emp_password=None):
        if emp_id is not None and emp_password is not None:
            try:
                emp = EmployeeInfo.objects.get(emp_id=emp_id)
                if emp.emp_password == emp_password:
                    return emp
            except EmployeeInfo.DoesNotExist:
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
