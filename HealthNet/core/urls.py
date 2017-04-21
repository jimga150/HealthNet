from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from . import views

urlpatterns = [
    url(r'^register/', views.register_patient_page, name='register'),
    url(r'^patient/', views.patient_landing, name='patient'),
    url(r'^patients/', views.view_patients, name='view patients'),
    url(r'^update_self/', views.editownpatientprofile, name='update'),
    # url(r'^update_user/', views.editownpatientprofile, name='update user'),
    url(r'^update_med_info/(?P<patient_id>[0-9]+)/',
        views.EditPatientMediInfo.as_view(success_url=reverse_lazy('view patients')), name='update medical info for'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^export/', views.download, name='download'),
    url(r'^email/', views.email, name='email_info'),
    url(r'^landing/', views.landing, name='landing'),
    url(r'^nurse/', views.nurse_landing, name='nurse'),
    url(r'^doctor/', views.doctor_landing, name='doctor'),
    url(r'^hadmin/', views.admin_landing, name='admin'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^tests/', views.patient_tests, name='tests'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^logs/', views.logs, name='logs'),
    url(r'^upload_patient/', views.upload_patient_info, name='upload patient'),
    url(r'^staffregister/', views.registerStaff, name='staffregister'),
    url(r'^adminregister/', views.register_admin_page, name='adminregister'),
    url(r'^doctorregister/', views.register_doctor_page, name='doctorregister'),
    url(r'^nurseregister/', views.register_nurse_page, name='nurseregister'),
    url(r'^$', views.main, name='main')

]
