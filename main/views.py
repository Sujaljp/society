from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from main.forms import NewUserForm, ComplaintForm, NoticeForm, ServiceForm, VisitorForm, otpForm
from main.models import MainPage
from .models import MainPage, Notice, Staff, Profile, Service, Bills, Visitor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.db.models import F
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
import os
from twilio.rest import Client
import random
import http.client



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
        if newservice.service_name == '1':
            subject = newservice.user.username
            message = newservice.service_details
            from_email = settings.EMAIL_HOST_USER
            recievers = ['mihirbhatkar87@gmail.com']
            emailsending = EmailMessage(subject, message, from_email, recievers)
            emailsending.send()
        if newservice.service_name == '2':
            subject = newservice.user.username
            message = newservice.service_details
            from_email = settings.EMAIL_HOST_USER
            recievers = ['21rihim@gmail.com']
            emailsending = EmailMessage(subject, message, from_email, recievers)
            emailsending.send()
        if newservice.service_name == '3':
            subject = newservice.user.username
            message = newservice.service_details
            from_email = settings.EMAIL_HOST_USER
            recievers = ['nishchayrajpal8@gmail.com']
            emailsending = EmailMessage(subject, message, from_email, recievers)
            emailsending.send()

        messages.info(request, 'Service has been notified of your request.')
        return redirect('main:homepage')




def test(request):
    obj = Service.objects.all()
    v1 = obj[0].service_name
    v2 = obj[1].service_name
    v3 = obj[2].service_name
    return render(request, 'main/test.html', context={'v1':v1, 'v2':v2, 'v3':v3})

def viewbill(request, bill_id):

    bill = model_to_dict(Bills.objects.get(pk = bill_id))

    username = request.user.get_username()
    for user1 in Profile.objects.all():
        if username == user1.user.username:
            prof = user1

    total = bill['repairs_maintenance_charges'] + bill['society_service_charges'] + bill['charity_charges'] + bill['sinking_fund_charges'] + bill['parking_charges']
    final = total + bill['previous_dues']

    context={'bill':bill, 'profile':prof, 'total':total, 'final':final}

    return render(request, 'main/viewbill.html', context )


def searchbill(request):
    obj = Profile.objects.all()
    x = 0 #for checking if user has bills or not
    username = request.user.get_username()
    list = []
    for user1 in Bills.objects.all():
        if username == user1.user.username:
            list.append(user1)
            x=1
    if x==1:
        return render(request, 'main/searchbill.html', context={'searchbill':list})
    if x==0:
        return render(request, 'main/nobills.html')

def addvisitor(request):
    if request.method == 'GET':
        return render(request, "main/addvisitor.html", context={'form': VisitorForm()})
    else:
        form = VisitorForm(request.POST)
        global newvisitor
        newvisitor = form.save(commit=False)
        newvisitor.user = request.user
        phone_no = newvisitor.visitor_phone
        
        check_flat = Profile.objects.filter(flat_no = newvisitor.visiting_flat).first()
        if check_flat:
            print('Testing')
        else:
            
            messages.error(request,'No such flat exists')
            return redirect('main:homepage')
        
        global otp
        otp = str(random.randint(1000, 9999))
        vlist = {'phone_no':phone_no, 'otp':otp}
        
        
        sms(phone_no, otp)
        
        request.session['phone_no'] = phone_no
        
        
        return redirect('main:otpfunc')

    

def otpfunc(request):
    mobile = request.session['phone_no']
    form = otpForm(request.POST)
    context = {'mobile':mobile, 'form':otpForm()}
    if request.method == 'GET':
        return render(request,'main/visitorotp.html', context)  
    else:
        otpnew = request.POST.get('otp')
        print(otp)
        print(otpnew)
        if otpnew == otp:
            newvisitor.save()
            messages.info(request, 'Visitor registered successfully!')
            return redirect('main:homepage')
        else:
            messages.error(request, 'Wrong otp entered!')
            return render(request,'main/home.html', context) 


def sms(mobile, otp):
     
 
    account_sid = 'AC1be04f78c7992d2b8bbe64386ae1a190' 
    auth_token = '999a81fa80b934dad00fc9e8524f7720' 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
                                messaging_service_sid='MG9217aa22b3c308b0a0c298d1aa79ce50', 
                                body=f'The otp is {otp}',      
                                to=f'{mobile}'
                            ) 
    
    print(message.sid)


def send_otp(mobile , otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    print('works')
    authkey = settings.AUTH_KEY
    payload = "{\"Value1\":\"Param1\",\"Value2\":\"Param2\",\"Value3\":\"Param3\"}"
    newmobile = str(mobile)
    newotp = str(otp)
    headers = { 'Content-Type': "application/json" }
    url1 ="https://api.msg91.com/api/v5/otp?otp="+otp+"&message="+"Your%20otp%20is%20"+newotp+"&mobile="+newmobile+"&authkey="+authkey+"&country=+91"
    conn.request("GET",url1, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None

def visitor(request):
    messages.info(request, 'You are viewing the Visitor Log')
    return render(request, "main/visitor.html", context={'visit': Visitor.objects.all})
