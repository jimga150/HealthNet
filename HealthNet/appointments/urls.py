from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^appointments/', views.appointment_main, name='appointment_home'),
    url(r'^appointment/create/$', views.CreateAppointment, name='appointment_create'),
    url(r'^edit/(?P<pk>[0-9]+)/', views.EditAppointment.as_view(), name='appointment_edit'),
    url(r'delete/(?P<pk>[0-9]+)/', views.DeleteAppointment.as_view(), name='delete'),
]
