from django.contrib import admin
from django.contrib.admin.helpers import Fieldset
from django.db.models import fields
from tinymce.widgets import TinyMCE
from django.db import models
from .models import MainPage, Profile, Notice, Complaint, Staff, Service, Bills

class MainPageAdmin(admin.ModelAdmin):
    fields = ['society_name',
              'society_about'
              ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }



admin.site.register(Profile)
admin.site.register(Notice)
admin.site.register(Complaint)
admin.site.register(Staff)
admin.site.register(Service)
admin.site.register(Bills)
