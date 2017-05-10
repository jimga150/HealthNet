from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^transfer/$', views.transfer_main, name='transfer_landing'),
    url(r'^transfer/confirmation/$', views.confirmation, name='transfer_confirmation'),
    url(r'^transfer/create/$', views.create, name='transfer_create')
]