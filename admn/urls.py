from django.urls import path,include
from . import views

urlpatterns = [
                path('',views.admnindex,name="admnindex"),
                path('inner',views.admninner,name="admninner"),
                path('logout',views.admnlogout,name="admnlogout"),
                path('addhr',views.addhr,name="addhr"),
                path('gomainmenu',views.gomainmenu,name="gomainmenu"),
                path('admnviewemp',views.admnviewemp,name="admnviewemp"),
                path('admnsendreminder',views.admnsendreminder,name="admnsendreminder"),
                path('viewdailylogdetails',views.viewdailylogdetails,name="viewdailylogdetails"),
                path('viewdailylogindetails',views.viewdailylogindetails,name="viewdailylogindetails"),
                path('viewdailylogoutdetails',views.viewdailylogoutdetails,name="viewdailylogoutdetails"),
                path('attendanceregister',views.attendance_register,name="attendanceregister"),
                path('checklogedlocation',views.checklogedlocation,name="checklogedlocation"),
                path("calculatesalary",views.calculatesalary,name="calculatesalary"),



]