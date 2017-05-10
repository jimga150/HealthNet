from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^messages/$', views.index, name='messages_home'),
    url(r'^messages/create/$', views.createMessage, name='messages_create'),
    url(r'^messages/editMessage/(?P<pk>[0-9]+)/', views.UpdateMessage.as_view(), name='messages_edit'),
    url(r'^messages/deleteMessage/(?P<pk>[0-9]+)/$', views.DeleteMessage.as_view(), name='messages_delete'),
]
