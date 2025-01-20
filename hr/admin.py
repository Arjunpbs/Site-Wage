from django.contrib import admin
from . models import SalaryInfo,HrInfo
from employee . models import EmployeeInfo

# Register your models here.
admin.site.register(SalaryInfo)
admin.site.register(HrInfo)
