from django.shortcuts import render,redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib import messages
from .models import Record
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,template_name='index.html')

#Register User

def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,"Account Created Successfully")
            return redirect("my-login")
    context = {"form":form}
    return  render(request,"register.html",context=context)

#login a user

def my_login(request):
    form  = LoginForm

    if request.method == "POST":
        form = LoginForm(request,data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context ={"form":form}
    return  render(request,template_name="my-login.html", context=context)


#dashboard
@login_required(login_url="my-login")
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records':my_records}
    return render(request,template_name="dashboard.html",context=context)

#create a record
@login_required(login_url="my-login")
def create_record(request):
    form = CreateRecordForm

    if request.method == "POST":
        form = CreateRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record created added successfully")

            return redirect("dashboard")

    context = {"form":form}

    return  render(request,template_name="create-record.html", context=context)

# update a record

def update_record(request,pk):
    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == "POST":
        form = UpdateRecordForm(request.POST,instance=record)

        if form.is_valid():
            form.save()

            messages.success(request, "Your records are updated")

            return redirect("dashboard")

    context={'form':form}
    return render(request,template_name="update-record.html", context=context)


#read/view a singular record

def singular_record(request,pk):
    all_records = Record.objects.get(id=pk)

    context = {"record":all_records}
    return render(request,template_name="view-record.html",context=context)


#delete record
@login_required(login_url="my-login")
def delete_record(request,pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request,"Deleted Record Successfully")
    return redirect('dashboard')

# user logout

def user_logout(request):
    auth.logout(request)
    messages.success(request,"Logout Successfully")

    return redirect('my-login')


