from django.db import models
from django.db.models.fields import CharField, TextField, EmailField, IntegerField
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from datetime import datetime
import datetime
class MainPage(models.Model):
    society_name = CharField(max_length=200)
    society_about = TextField()

    def __str__(self):
        return self.society_name

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    age = models.IntegerField(blank=True)
    flat_no = models.CharField(max_length=10)
    phone_number = models.IntegerField()

    def __str__(self):
        return str(self.flat_no)


class Notice(models.Model):
    header_notice = CharField(max_length=100)
    details_notice = TextField()

    def __str__(self):
        return self.header_notice

class Complaint(models.Model):
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    content = models.TextField()
    complaint_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.contact_name)

class Staff(models.Model):
    staff_name = models.CharField(max_length=100)
    staff_email = models.EmailField()
    staff_phone = models.IntegerField()
    designation = models.CharField(max_length=100)
    about = models.TextField(null=True)
    image = models.ImageField(upload_to='main/images')
    def __str__(self):
        return str(self.designation)

class Visitor(models.Model):
    visitor_name = models.CharField(max_length=100)
    visitor_phone =  models.IntegerField()
    visiting_flat = models.CharField(max_length=100)
    visiting_date = models.DateField(default=datetime.date.today)
    visiting_time = models.TimeField(default=datetime.datetime.now)
    def __str__(self):
        return str(self.visitor_name)



class Service(models.Model):
    service_name=models.CharField(max_length=100)
    service_email=models.EmailField(null=True)
    service_details=models.TextField(blank=True)
    def __str__(self):
        return str(self.service_name)


class Bills(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    repairs_maintenance_charges = models.IntegerField()
    society_service_charges = models.IntegerField()
    sinking_fund_charges = models.IntegerField(default=80)
    parking_charges = models.IntegerField(default=100)
    charity_charges = models.IntegerField(default=20)
    previous_dues = models.IntegerField(default=0, null=True)

    publish_date = models.DateField(default=datetime.date.today, blank=True)
    due_date = models.DateField()
    flat_no_and_date = models.CharField(max_length=100)
    def __str__(self):
        return str(self.flat_no_and_date)
