

# Create your models here.
from django.db import models
from employee . models import EmployeeInfo
class SalaryInfo(models.Model):
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)
    basic_salary= models.DecimalField(max_digits=10, decimal_places=2)

class HrInfo(models.Model):
    hr_id = models.CharField(max_length=20, unique=True)
    hr_name = models.CharField(max_length=150)
    hr_phone = models.CharField(max_length=50)
    hr_email = models.EmailField()
    hr_addres = models.CharField(max_length=250)
    hr_password = models.CharField(max_length=150)
    last_login = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.hr_id





   