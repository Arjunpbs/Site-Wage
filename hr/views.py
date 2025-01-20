from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from employee . models import EmployeeInfo
from django.core.exceptions import ObjectDoesNotExist
from . models import SalaryInfo,HrInfo
# Create your views here.


def index(request):
    return render(request,'index.html')



def handlelogin(request):
    if request.method == "POST":
        hr_id = request.POST.get('username', '')
        hr_password = request.POST.get('password', '')
        if hr_id and hr_password:
            hr = authenticate(hr_id=hr_id, hr_password=hr_password)
            if hr is not None:
                login(request, hr)
                return redirect('inner')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Please provide both username and password")
    return redirect('index')

   

def innerpage(request):
	return render(request,"inner.html")



def handlelogout(request):
    logout(request)
    messages.error(request,"Successfully Logout")
    return redirect("index")

def addemployee(request):
    if request.method == "POST":
        emp_id = request.POST.get('emp_id', '')
        emp_name = request.POST.get('emp_name', '')
        emp_phone = request.POST.get('emp_phone', '')
        emp_email =request.POST.get('emp_email','')
        emp_address = request.POST.get('emp_address','')
        emp_job = request.POST.get('emp_job','')
        emp_department = request.POST.get('emp_department','')
        emp_password = request.POST.get('emp_password','')

        
        existing_employee_id = EmployeeInfo.objects.filter(emp_id=emp_id).exists()
        if existing_employee_id:
                messages.error(request, "Employee with this ID already exists!")
                return redirect('addemployee')

        
        existing_employee_phone = EmployeeInfo.objects.filter(emp_phone=emp_phone).exists()
        if existing_employee_phone:
                        messages.error(request, "Employee with this phone number already exists!")
                        return redirect('addemployee')

        
        existing_employee_email = EmployeeInfo.objects.filter(emp_email=emp_email).exists()
        if existing_employee_email:
                    messages.error(request, "Employee with this email already exists!")
                    return redirect('addemployee')
        
        new_employee = EmployeeInfo(
                emp_id=emp_id,
                emp_name=emp_name,
                emp_phone=emp_phone,
                emp_email=emp_email,
                emp_addres=emp_address,
                emp_job=emp_job,
                emp_department=emp_department,
                emp_password=emp_password
            )
            
        new_employee.save()
        messages.error(request,"Successfully Added Employee Details")
        return redirect('addemployee')

    return render(request,'addemp.html')


def gotomainmenu(request):
    return redirect('inner')

def editemployee(request):
    if request.method =="POST":
         emp_id = request.POST.get('emp_id', '')
         print(emp_id)
         try:
                tobeedit = EmployeeInfo.objects.get(emp_id=emp_id)
                print(tobeedit)
                return render(request,'editemp.html',{'employee':tobeedit})
                
         except ObjectDoesNotExist:
                
                messages.error(request, 'Please enter a valid Employee ID.')
                return render(request,"editemp.html")
    return render(request,"editemp.html")


def update_employee(request):
     if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        employee = EmployeeInfo.objects.get(emp_id=emp_id)
        
        
        employee.emp_name = request.POST.get('emp_name')
        employee.emp_phone = request.POST.get('emp_phone')
        employee.emp_email = request.POST.get('emp_email')
        employee.emp_addres = request.POST.get('emp_addres')
        employee.emp_job = request.POST.get('emp_job')
        employee.emp_department = request.POST.get('emp_department')
        employee.emp_password = request.POST.get('emp_password')
        employee.save()
        messages.error(request, 'Succesfull Edited Employee Details.')
     return redirect('editemployee')



def  addsalarydetails(request):
     if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        basicsalary = request.POST.get('basicsalary')
        bonus=request.POST.get('bonus')
        try:
                employee_instance = EmployeeInfo.objects.get(emp_id=emp_id)
                new_salary = SalaryInfo.objects.create(
                        employee=employee_instance,
                        basic_salary=basicsalary,
                        bonus=bonus
                    )
                messages.error(request, 'Salary Added Successfully')
                return render(request,'addsalary.html')
        except ObjectDoesNotExist:
                
                messages.error(request, 'Please enter a valid Employee ID.')
                return render(request,"addsalary.html")
           
     return render(request,'addsalary.html')



def editsalary(request):
    if request.method == "POST":
        emp_id = request.POST.get('emp_id')
        try:
            empinstance = EmployeeInfo.objects.get(emp_id=emp_id)
            salary_details = SalaryInfo.objects.filter(employee=empinstance)
            print(salary_details)
            return render(request, 'editsal.html', {'empinstance': empinstance,'salary_details': salary_details})
        except ObjectDoesNotExist:
            messages.error(request, 'Enter valid Emp_Id')
            return render(request, 'editsal.html')

    return render(request, "editsal.html")

def update_empsalary(request):
      if request.method == 'POST':
            emp_id = request.POST.get('emp_id')
            empinstance = EmployeeInfo.objects.get(emp_id=emp_id)
            salary_details = SalaryInfo.objects.filter(employee=empinstance)
            salary_details = salary_details.first()
            salary_details.bonus=request.POST.get('bonus')
            salary_details.basic_salary=request.POST.get('basic_salary')
            salary_details.save()
            messages.error(request, 'Succesfull Edited Salary Details.')
      return redirect('editsalary')

def viewemplist(request):
     employees = EmployeeInfo.objects.all()
     employee_salary = {}
     for employee in employees:
        salary_info = SalaryInfo.objects.filter(employee=employee).first()
        employee_salary[employee] = salary_info
     return render(request, 'emplist2.html', {'employee_salary': employee_salary})
    
     
	
