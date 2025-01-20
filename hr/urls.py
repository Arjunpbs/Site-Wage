from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('login',views.handlelogin,name="login"),
    path('inner',views.innerpage,name="inner"),
    path('logout',views.handlelogout,name="logout"),
    path('addemployee',views.addemployee,name="addemployee"),
    path('gotomainmenu',views.gotomainmenu,name="gotomainmenu"),
    path('editemployee',views.editemployee,name="editemployee"),
    path('update_employee',views.update_employee,name="update_employee"),
    path('addsalarydetails',views.addsalarydetails,name="addsalarydetails"),
    path('editsalary',views.editsalary,name="editsalary"),
    path('update_empsalary',views.update_empsalary,name="update_empsalary"),
    path('viewemplist',views.viewemplist,name="viewemplist"),
]