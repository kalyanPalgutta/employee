from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from . import forms, models
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,HttpResponse
from.models import *
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, "index.html")

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/updateinput")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

class InsertInput(View):
    def get(self,request):
        return render(request, 'Employeeinput.html')
class InserView(View):
    def get(self,request):
        Employee_Id = int(request.GET["t1"])
        Employee_name = request.GET["t2"]
        Employee_Designation = request.GET["t3"]
        Joined_Date = request.GET["t4"]
        Employee_Address = request.GET["t5"]
        Employee_Phone = request.GET["t6"]
        Employee_Email = request.GET["t7"]
        Employee_Salary = request.GET["t8"]
        Employee_WorkingDays = request.GET["t9"]

        p1=Details(EmployeeId=Employee_Id,EmployeeName=Employee_name,Designation=Employee_Designation,JoinedDate=Joined_Date,Address=Employee_Address,Phone=Employee_Phone,Email=Employee_Email,Salary=Employee_Salary,WorkingDays=Employee_WorkingDays)
        p1.save()
        resp=HttpResponse("Employee inserted successfully")
        return resp
class DisplayView(View):
    def get(self,request):
        if 'q' in request.GET:
            q = request.GET['q']
            multiple_q = Q(Q(EmployeeId__icontains=q) | Q(EmployeeName__icontains=q))
            qs = Details.objects.filter(multiple_q)
        else:
            qs = Details.objects.all()

        con_dic={"records":qs}
        return render(request,"display.html",con_dic)

class UpdateInputView(View):
    def get(self,request):
        return render(request,"updateinput.html")
class UpdateView(View):
    def post(self,request):
        Employee_Id=int(request.POST["t1"])
        Employee_name = request.POST["t2"]
        Employee_Designation = request.POST["t3"]
        Joined_Date = request.POST["t4"]
        Employee_Address=request.POST["t5"]
        Employee_Phone = request.POST["t6"]
        Employee_Email = request.POST["t7"]
        Employee_Salary = request.POST["t8"]
        Employee_WorkingDays = request.POST["t9"]
        Empl=Details.objects.get(EmployeeId=Employee_Id)
        Empl.EmployeeName=Employee_name
        Empl.Designation=Employee_Designation
        Empl.JoinedDate=Joined_Date
        Empl.Address=Employee_Address
        Empl.Phone=Employee_Phone
        Empl.Email = Employee_Email
        Empl.Salary = Employee_Salary
        Empl.WorkingDays = Employee_WorkingDays

        Empl.save()
        resp = HttpResponse("Employee updated successfully")
        return resp

class DeleteInputView(View):
    def get(self,request):
        return render(request,"deleteinput.html")
class DeleteView(View):
    def get(self,request):
        Employee_Id=int(request.GET["t1"])
        Emp=Details.objects.filter(EmployeeId=Employee_Id)
        Emp.delete()
        resp = HttpResponse("Employee deleted successfully")
        return resp

def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "change_password.html")

def Logout(request):
    logout(request)
    return redirect ("/")