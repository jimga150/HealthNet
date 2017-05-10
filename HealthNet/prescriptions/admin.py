from django.contrib import admin

# Register your models here.
from prescriptions.models import Prescription

admin.site.register(Prescription)
