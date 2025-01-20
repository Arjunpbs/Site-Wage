# employee/models.py
from django.db import models
from django.db.models import UniqueConstraint


class EmployeeInfo(models.Model):
    emp_id = models.CharField(max_length=20, unique=True)
    emp_name = models.CharField(max_length=150)
    emp_phone = models.CharField(max_length=50)
    emp_email = models.EmailField()
    emp_addres = models.CharField(max_length=250)
    emp_job = models.CharField(max_length=50)
    emp_password = models.CharField(max_length=150)
    emp_department = models.CharField(max_length=150)
    last_login = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.emp_id

from django.utils import timezone


class Submission(models.Model):
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='submissions/')
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    saved_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        local_time = timezone.localtime(self.saved_datetime)
        return f"Submission by {self.employee.emp_name} at {local_time}"



class logotsave(models.Model):
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    saved_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        local_time = timezone.localtime(self.saved_datetime)
        return f"Submission by {self.employee.emp_name} at {local_time}"


    
class Threehourlocation(models.Model):
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    saved_datetime = models.DateTimeField(default=timezone.now)
    def __str__(self):
        local_time = timezone.localtime(self.saved_datetime)
        return f"Submission by {self.employee.emp_name} at {local_time}"
