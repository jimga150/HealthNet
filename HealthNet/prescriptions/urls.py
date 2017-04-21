from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^prescriptions/', views.prescriptions, name='prescriptions'),
    url(r'^new_prescription/', views.new_prescription, name='new prescription'),
    url(r'^delete_prescription/(?P<prescription_id>[0-9]+)/', views.delete_prescription, name='delete prescription'),
    url(r'^patient_prescriptions/(?P<patient_id>[0-9]+)/', views.prescriptions_list,
        name='list prescriptions for patient')
    ]
