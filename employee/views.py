

# Create your views here.
# employee/views.py
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import authenticate, login,logout
from . models import EmployeeInfo,Submission,logotsave,Threehourlocation
from django.contrib import messages
import base64
from django.core.files.base import ContentFile
from django.utils.timezone import now
from .authentication import EmployeeBackend
from admn .models import Reminder
from .utils import encrypt, decrypt
from django.core.files.base import ContentFile
from django.utils.timezone import now


def empindex(request):
    if request.method=="POST":
        emp_id=request.POST["username"]
        emp_password=request.POST["password"]
        if emp_id and emp_password:
            emp = authenticate(emp_id=emp_id,emp_password=emp_password)
           
            if emp is not None:
                login(request,emp)
                emp_id = encrypt(emp_id)
                return redirect(reverse('empinner', kwargs={'emp_id': emp_id}))

            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Please provide both username and password")
    return render(request,"empindex.html")


def emplogout(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        logged_in_employee = EmployeeInfo.objects.get(emp_id=emp_id)
        if logged_in_employee is not None:
            if request.session.get('attendance_submitted', False):
                latitude = request.POST.get('latitude')
                longitude = request.POST.get('longitude')
                logsave=logotsave.objects.create(employee=logged_in_employee,latitude=latitude,
                        longitude=longitude)
                print(f"Employee ID: {emp_id}, Latitude: {latitude}, Longitude: {longitude}")
                print("successfully saved")
            request.session['attendance_submitted'] = False
    logout(request)
    messages.error(request,"Successfully Logout")
    return redirect('empindex')



def submit_form(request):
    if request.method == 'POST':
         emp_id = request.POST.get('emp_id')
         logged_in_employee = EmployeeInfo.objects.get(emp_id=emp_id)
         if logged_in_employee is not None:
                image_data = request.POST.get('image')
                lat = request.POST.get('latitude')
                long = request.POST.get('longitude')
                format, imgstr = image_data.split(';base64,') 
                ext = format.split('/')[-1]
                image_data = ContentFile(base64.b64decode(imgstr), name=f"{now()}.{ext}")
                submission = Submission.objects.create(
                    employee=logged_in_employee,
                    image=image_data,
                    latitude=lat,
                    longitude=long
                )
                print("success fully added")
                messages.error(request,"Attendance Added Successfully")
                request.session['attendance_submitted'] = True
                emp_id = encrypt(emp_id)
                return redirect(reverse('empinner', kwargs={'emp_id': emp_id}))


         else:
                print("not getting emp inner loged emp details") 
                messages.error(request," Oops Something Went Wrong Check Internet Connection !")
                return redirect('empindex')
    emp_id = encrypt(emp_id)
    return redirect(reverse('empinner', kwargs={'emp_id': emp_id}))

   

def empinner(request,emp_id):
    try:
        decrypted_emp_id = decrypt(emp_id)
        print(decrypted_emp_id)
        emp = EmployeeInfo.objects.get(emp_id=decrypted_emp_id)
        reminders = Reminder.objects.filter(employee=emp).order_by('-created_at')
        return render(request, "empinner.html", {'reminders': reminders, 'emp': emp})
    except Exception as e:
        messages.error(request, "Invalid or corrupted employee ID")
        return redirect('empindex')


def threehoursave(request):
    if request.method == 'POST':
         emp_id = request.POST.get('emp_id')
         employee = EmployeeInfo.objects.get(emp_id=emp_id)
         if employee is not None:
             lat = request.POST.get('latitude')
             long = request.POST.get('longitude')
             obj=Threehourlocation.objects.create(
                 employee=employee,
                    latitude=lat,
                    longitude=long
                 
             )
             print("success fully added threehoursave")
    else:
                print("not getting emp inner loged emp details") 
    emp_id = encrypt(emp_id)
    return redirect(reverse('empinner', kwargs={'emp_id': emp_id}))
             
