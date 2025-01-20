from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from hr . models import HrInfo
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from employee . models import EmployeeInfo,Submission,logotsave,Threehourlocation
from hr .models import SalaryInfo,HrInfo
from . models import Reminder,Attendance
from django.utils import timezone


# Create your views here.
def admnindex(request):
        if request.method == "POST":
                admn_id = request.POST.get('admn_id', '')
                admn_password = request.POST.get('admn_password', '')
                if admn_id and admn_password:
                        admn = authenticate(admn_id=admn_id, admn_password=admn_password)
                        if admn is not None:
                                login(request, admn)
                                return redirect('admninner')
                        else:
                                messages.error(request, "Invalid username or password")
                else:
                        messages.error(request, "Please provide both username and password")
        return render(request,"admnindex.html")
    
def admninner(request):
        return render(request,'admninner.html')

def admnlogout(request):
        logout(request)
        messages.error(request,"Successfully Logout")
        return redirect("admnindex")

def addhr(request):
        if request.method == "POST":
                hr_id = request.POST.get('hr_id', '')
                hr_name = request.POST.get('hr_name', '')
                hr_phone = request.POST.get('hr_phone', '')
                hr_email =request.POST.get('hr_email','')
                hr_address = request.POST.get('hr_address','')
                hr_password = request.POST.get('hr_password','')
                try:
                        existing_hr = HrInfo.objects.get(hr_id=hr_id)
                        messages.error(request,"HR with this ID already exists!")
                        return redirect('addhr')
                
                except HrInfo.DoesNotExist:
        
                        new_hr = HrInfo(
                                hr_id=hr_id,
                                hr_name=hr_name,
                                hr_phone=hr_phone,
                                hr_email=hr_email,
                                hr_addres=hr_address,
                                hr_password=hr_password
                        )
                        print(hr_id)
                        new_hr.save()
                        messages.error(request,"Successfully Added Employee Details")
                        return redirect('addhr')
        return render(request,'addhr.html')

def gomainmenu(request):
        return redirect('admninner')

def admnviewemp(request):
    employees = EmployeeInfo.objects.all()
    employee_salary = {}
    for employee in employees:
        salary_info = SalaryInfo.objects.filter(employee=employee).first()
        employee_salary[employee] = salary_info
    return render(request, 'emplist.html', {'employee_salary': employee_salary})

def admnsendreminder(request):
       if request.method == "POST":
                emp_id = request.POST.get('emp_id', '')
                reminder = request.POST.get('reminder', '')
                if emp_id.lower() != "all":
                        try:
                                employee = EmployeeInfo.objects.get(emp_id=emp_id)
                        except:
                                 messages.error(request, 'Please Provide Valid Data')
                                 return redirect('admnsendreminder')


                if emp_id.lower() == 'all':  
                        employees = EmployeeInfo.objects.all()
                        for employee in employees:
                                Reminder.objects.create(employee=employee, reminder_text=reminder)
                        messages.error(request, 'Reminder Sended Successfully')
                elif employee is not None:
                        employee = EmployeeInfo.objects.get(emp_id=emp_id)
                        Reminder.objects.create(employee=employee, reminder_text=reminder)
                        messages.error(request, 'Reminder Sended Successfully')
                else:
                         messages.error(request, 'Please Provide Valid Data')
        
       return render(request,"admnsendreminder.html")



from django.utils.timezone import now
from collections import defaultdict
from datetime import timedelta


def viewdailylogdetails(request):
    
    submissions = Submission.objects.all().order_by('-saved_datetime')
    logouts = logotsave.objects.all().order_by('-saved_datetime')
    logout_for_submission = defaultdict(list)
    
    for logout in logouts:
        local_logout_datetime = timezone.localtime(logout.saved_datetime)
        logout.saved_datetime = local_logout_datetime
        logout_for_submission[logout.employee.emp_id].append(logout)
    
    logs_by_date = defaultdict(list)
    
    for submission in submissions:
        emp_id = submission.employee.emp_id
        logout = None
        local_submission_datetime = timezone.localtime(submission.saved_datetime)
        submission.saved_datetime = local_submission_datetime
        
        for log in logout_for_submission[emp_id]:
            if log.saved_datetime.date() == submission.saved_datetime.date():
                logout = log
                logout_for_submission[emp_id].remove(log)
                break
        
        log_entry = {
            'submission': submission,
            'logout': logout,
        }
        logs_by_date[submission.saved_datetime.date()].append(log_entry)
    sorted_logs_by_date = sorted(logs_by_date.items(), key=lambda x: x[0], reverse=True)
    
    context = {
        'logs_by_date': sorted_logs_by_date,
    }
    
    return render(request, 'viewlogdetails.html', context)

from django.utils import timezone
from datetime import datetime

       
def viewdailylogindetails(request):
    submissions = Submission.objects.select_related('employee').order_by('-saved_datetime')
    submissions_by_date = defaultdict(list)
    
    for submission in submissions:
        local_submission_datetime = timezone.localtime(submission.saved_datetime)
        submission.saved_datetime = local_submission_datetime
        submissions_by_date[local_submission_datetime.date()].append(submission)

    sorted_submissions_by_date = sorted(submissions_by_date.items(), key=lambda x: x[0], reverse=True)
    
    for date, submissions in sorted_submissions_by_date:
        print(f"Date: {date}")
        for submission in submissions:
            print(f"{submission.employee.emp_name} at {submission.saved_datetime}")

    return render(request, "viewdailyloginloc.html", {'sorted_submissions_by_date': sorted_submissions_by_date})

def viewdailylogoutdetails(request):
    logoutsaves = logotsave.objects.select_related('employee').order_by('-saved_datetime')
    logoutsaves_by_date = defaultdict(list)
    
    for logoutsave in logoutsaves:
        local_logout_datetime = timezone.localtime(logoutsave.saved_datetime)
        logoutsave.saved_datetime = local_logout_datetime
        logoutsaves_by_date[local_logout_datetime.date()].append(logoutsave)
    
    sorted_logoutsaves_by_date = sorted(logoutsaves_by_date.items(), key=lambda x: x[0], reverse=True)
    
    return render(request, "viewdailylogoutloc.html", {'sorted_logoutsaves_by_date': sorted_logoutsaves_by_date})

def attendance_register(request):
    employees = EmployeeInfo.objects.all()
    date = timezone.localtime().date()
    print(date)
    attendances = {}

    for employee in employees:
        attendance, created = Attendance.objects.get_or_create(employee=employee, date=date, defaults={'status': 'A'})
        attendances[employee.emp_id] = attendance.status
        employee.attendance_status = attendance.status  

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        attendance = get_object_or_404(Attendance, employee__emp_id=employee_id, date=date)
        attendance.status = 'P' if attendance.status == 'A' else 'A'
        attendance.save()
        return redirect('attendanceregister')  

    
    all_attendance_records = Attendance.objects.exclude(date=date).order_by('-date')
    previous_attendances_by_date = defaultdict(list)
    for record in all_attendance_records:
        previous_attendances_by_date[record.date].append(record)

    context = {
        'employees': employees,
        'date': date,
        'attendances': attendances,
        'previous_attendances_by_date': dict(previous_attendances_by_date),
    }
    print("Context:", context)  
    return render(request, 'attendanceregister.html', context)

def checklogedlocation(request):
      context = {}
      if request.method == 'POST':
                emp_id = request.POST.get('emp_id')
                employee = get_object_or_404(EmployeeInfo, emp_id=emp_id)
                current_date = timezone.localtime().date()

        
                submission = Submission.objects.filter(employee=employee, saved_datetime__date=current_date).first()
        
        
                logout = logotsave.objects.filter(employee=employee, saved_datetime__date=current_date).first()
        
                if submission:
                        if logout:
                                context['status'] = f"Employee {employee.emp_name} has submitted photo and location for attendance today and  logged out."
                        else:
                                latest_location = Threehourlocation.objects.filter(employee=employee).order_by('-saved_datetime').first()
                                if latest_location:
                                       return render(request,"checkloc.html",{'latest_location': latest_location})
                                else:
                                        context['status'] = f"Employee {employee.emp_name} is currently logged in. No location updates found."
        
                else:
                        context['status'] = f"Employee {employee.emp_name} has not submitted photo and location for attendance today."

      return render(request,'check_loged_location.html', context)


from django.db.models import Count, Q
import calendar




def calculatesalary(request):
    current_date = timezone.localtime()
    current_year = current_date.year
    current_month = current_date.month
    
    attendance_data = Attendance.objects.values(
        'employee__emp_id', 
        'employee__emp_name', 
        'employee__emp_department', 
        'employee__emp_job', 
        'date__year', 
        'date__month'
    ).annotate(
        present_count=Count('id', filter=Q(status='P')),
        absent_count=Count('id', filter=Q(status='A'))
    ).order_by('-date__year', '-date__month', 'employee__emp_id')
    
    summary = defaultdict(list)
    for record in attendance_data:
        emp_id = record['employee__emp_id']
        emp_name = record['employee__emp_name']
        emp_department = record['employee__emp_department']
        emp_job = record['employee__emp_job']
        year = record['date__year']
        month = record['date__month']
        
        try:
            salary_info = SalaryInfo.objects.get(employee__emp_id=emp_id)
        except SalaryInfo.DoesNotExist:
            pay_per_day = 0
            salary_for_month = 0
            bonus = 0
        else:
            days_in_month = calendar.monthrange(year, month)[1]
            pay_per_day = salary_info.basic_salary / days_in_month
            salary_for_month = pay_per_day * record['present_count']
            bonus = 0

            if record['present_count'] > 24:
                bonus = salary_info.bonus
        
        total_salary = salary_for_month + bonus
        
        month_name = calendar.month_name[month]
        
        summary[(year, month_name)].append({
            'emp_id': emp_id,
            'emp_name': emp_name,
            'emp_department': emp_department,
            'emp_job': emp_job,
            'present_count': record['present_count'],
            'absent_count': record['absent_count'],
            'pay_per_day': pay_per_day,
            'salary_for_month': salary_for_month,
            'bonus': bonus,
            'total_salary': total_salary
        })
    
    # Sort summary by year and month in descending order
    sorted_summary = sorted(summary.items(), key=lambda x: (x[0][0], list(calendar.month_name).index(x[0][1])), reverse=True)
    context = {'sorted_summary': sorted_summary}
    return render(request, 'calculatesalary.html', context)