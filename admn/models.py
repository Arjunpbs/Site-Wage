from django.db import models
from employee .models import EmployeeInfo

# Create your models here.
class AdminInfo(models.Model):
    admn_id = models.CharField(max_length=20, unique=True)
    admn_name = models.CharField(max_length=150)
    admn_phone = models.CharField(max_length=50)
    admn_email = models.EmailField()
    admn_addres = models.CharField(max_length=250)
    admn_password = models.CharField(max_length=150)
    last_login = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.admn_name

class Reminder(models.Model):
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE)
    reminder_text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Latest reminders first




from datetime import date
from django.utils import timezone


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
    ]
    
    employee = models.ForeignKey(EmployeeInfo, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.emp_name} - {self.date} - {self.status}"
