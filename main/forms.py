from django import forms
from django.forms import ModelForm
from .models import Complaint, Notice, Service
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField()
    flat_no = forms.CharField(max_length=10, required=True)
    phone_number = forms.IntegerField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", 'age', 'flat_no'
                , 'phone_number')
        def save(self, commit=True):
            user =  super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.age = self.cleaned_data['age']
            user.flat_no = self.cleaned_data['flat_no']
            user.phone_number = self.cleaned_data['phone_number']
            if commit:
                user.save()
            return user


class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['contact_name', 'contact_email', 'content']


    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "Please specify your complaint:"

class NoticeForm(ModelForm):
    class Meta:
        model = Notice
        fields = ['header_notice', 'details_notice']

    header_notice = forms.CharField(required=True)
    details_notice = forms.CharField(required=True,widget=forms.Textarea)


    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        self.fields['header_notice'].label = "Specify the subject:"
        self.fields['details_notice'].label = "Enter the content of the notice:"


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['service_name','client','service_details']

    demo_choice = (
                    ("1", "Electrician"),
                    ("2", "Internet Service Provider"),
                    ("3", "Plumber"),
                  )
    service_name = forms.ChoiceField(choices = demo_choice )
    client = forms.CharField(required=True)
    service_details = forms.CharField(required=True,widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['client'].label = "Please enter your Flat Number:"
        self.fields['service_details'].label = "Specify your request:"
