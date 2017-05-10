from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^testresults/$', views.index, name='results_home'),
    url(r'^testresults_patient/', views.view_for_patient, name='view test results for patient'),
    url(r'^testresults/create/$', views.createResult, name='results_create'),
    url(r'^testresults/editTest/(?P<pk>[0-9]+)/', views.UpdateTest.as_view(), name='results_edit'),
    url(r'^testresults/deleteTest/(?P<pk>[0-9]+)/', views.DeleteTest.as_view(), name='results_delete'),
]
