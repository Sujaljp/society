from django.shortcuts import render, redirect, get_object_or_404
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
from django.forms.models import model_to_dict
import razorpay
from django.views.decorators.csrf import csrf_exempt


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

    context={'bill':bill, 'profile':prof, 'total':total, 'final':final, 'bill_id': bill_id}

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

@csrf_exempt
def pay(request, bill_id):
    
    bill = model_to_dict(Bills.objects.get(pk = bill_id))

    username = request.user.get_username()
    for user1 in Profile.objects.all():
        if username == user1.user.username:
            prof = user1

    total = bill['repairs_maintenance_charges'] + bill['society_service_charges'] + bill['charity_charges'] + bill['sinking_fund_charges'] + bill['parking_charges']
    final = total + bill['previous_dues']

    context={'bill':bill, 'profile':prof, 'total':total, 'final':final, 'finalP': final*100}

    if request.method == 'POST':
        print(5)
        razorpay_client = razorpay.Client(auth=("rzp_test_CK8AWrEy84pP7i", "UNfgBNxADdlf1rb5rmU4UyPx"))   
        data = { "amount": final*100, "currency": "INR", "receipt": "order_rcptid_11", 'payment_capture': '1'}
        razorpay_order = razorpay_client.order.create(data=data)
        razorpay_order_id = razorpay_order['id']
    return render(request, 'main/pay.html', context)

@csrf_exempt
def success(request):
    return render(request, "main/success.html")

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
        