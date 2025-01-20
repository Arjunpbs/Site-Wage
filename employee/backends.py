# employee/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Employee

class EmployeeBackend(ModelBackend):
    def authenticate(self, request, empid=None, emp_password=None):
        try:
            employee = Employee.objects.get(empid=empid)
            if employee.check_password(emp_password):
                return employee
        except Employee.DoesNotExist:
            return None
