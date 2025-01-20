
from django.urls import path,include
from . import views
urlpatterns = [
            path('',views.empindex,name="empindex"),
            path('emplogout',views.emplogout,name="emplogout"),
            path('submit_form/', views.submit_form, name='submit_form'),
            path('empinner/<str:emp_id>/', views.empinner, name='empinner'),
            path('threehoursave/',views.threehoursave,name="threehoursave"),

           
]
