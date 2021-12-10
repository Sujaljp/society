from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.forms import NewUserForm, ComplaintForm, NoticeForm, ServiceForm
from main.models import MainPage
from .models import MainPage, Notice, Staff, Profile, Service, Bills
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.db.models import F
from django.contrib.auth.models import User
def homepage(request):
    return render(request=request,
                  template_name='main/home.html',
                  context={'mainpage': MainPage.objects.all})


def register(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'New Account Created!: {username}')
            login(request, user)
            messages.info(request, f'You are now logged in as: {username}')
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm
    return render(request, "main/register.html", context={'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect("main:homepage")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('main:homepage')
            else:
                messages.error(request, f'Invalid username or password')
        else:
            messages.error(request, f'Invalid username or password')

    form = AuthenticationForm()
    return render(request, "main/login.html", {'form': form})


def noticeboard(request):
    messages.info(request, 'You are viewing the Notice Board!')

    return render(request, "main/noticeboard.html", context={'noticeboard': Notice.objects.all})


def complaint(request):
    if request.method == 'GET':
        return render(request, "main/complaint.html", context={'form': ComplaintForm()})
    else:
        form = ComplaintForm(request.POST)
        newcomplaint = form.save(commit=False)
        newcomplaint.user = request.user
        newcomplaint.save()
        messages.info(request, 'Complaint registered successfully!')
        return redirect('main:homepage')


def staff(request):
    staff = Staff.objects.all()
    return render(request, "main/staff.html", context={'staff': staff})


def makenotice(request):
    note = Notice()
    if request.method == 'GET':
        return render(request, "main/makenotice.html", context={'form': NoticeForm()})
    else:
        form = NoticeForm(request.POST)
        newnotice = form.save(commit=False)
        newnotice.user = request.user

        subject = newnotice.header_notice
        message = newnotice.details_notice
        from_email = settings.EMAIL_HOST_USER
        recievers = []
        for user1 in Profile.objects.all():
            recievers.append(user1.email)
        emailsending = EmailMessage(subject, message, from_email, recievers)
        emailsending.send()

        newnotice.save()
        messages.info(request, 'Notice made successfully!')
        return redirect('main:homepage')

def service(request):
    if request.method == 'GET':
        return render(request, "main/service.html", context={'form': ServiceForm()})
    else:

        form = ServiceForm(request.POST)
        newservice = form.save(commit=False)
        newservice.user = request.user
        newservice.save()




        messages.info(request, 'Service has been notified of your request.')
        return redirect('main:homepage')




def test(request):
    obj = Service.objects.all()
    v1 = obj[0].service_name
    v2 = obj[1].service_name
    v3 = obj[2].service_name
    return render(request, 'main/test.html', context={'v1':v1, 'v2':v2, 'v3':v3})

def viewbill(request, list):
    obj = Bills.objects.all()

    importlist = searchbill(list)
    print(importlist)





    repairs_maintenance_charges = obj.repairs_maintenance_charges
    society_service_charges = obj.society_service_charges
    sinking_fund_charges = obj.sinking_fund_charges
    charity_charges = obj.charity_charges
    parking_charges = obj.parking_charges
    summation = repairs_maintenance_charges+society_service_charges+parking_charges+charity_charges+sinking_fund_charges

    context={'searchbill':Bills.objects.all(),
             'summation':summation,
             'profile':Profile.objects.all()}
    return render(request, 'main/viewbill.html', context )


def searchbill(request):
    obj = Profile.objects.all()
    username = request.user.get_username()
    list = []
    for user1 in Bills.objects.all():
        if username == user1.user.username:
            list.append(user1)

    return list
    return render(request, 'main/searchbill.html', context={'searchbill':list})
