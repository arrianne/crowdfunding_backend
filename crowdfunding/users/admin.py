from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Fundraiser, Pledge

admin.site.register(Fundraiser)
admin.site.register(Pledge)
