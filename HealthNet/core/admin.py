from django.contrib import admin
from .models import *

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Admin)
admin.site.register(Hospital)
admin.site.register(Log)
