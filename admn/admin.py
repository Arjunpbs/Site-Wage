from django.contrib import admin
from . models import AdminInfo,Attendance,Reminder


# Register your models here.
admin.site.register(AdminInfo)
admin.site.register(Attendance)
admin.site.register(Reminder)

