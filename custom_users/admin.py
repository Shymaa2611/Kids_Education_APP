from django.contrib import admin
from .models import customuser,Verification,Kid,Profile



admin.site.register(customuser)
admin.site.register(Verification)
admin.site.register(Kid)
admin.site.register(Profile)