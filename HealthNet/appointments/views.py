import datetime

from core.models import Log
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from core.views import is_doctor, is_patient, is_admin
from .forms import AppointmentForm
from .models import Appointment


def is_doc_or_patient(user):
    """
    Helper function that checks if a user is a doctor or a patient
    :param user: The user to be checked
    :return: True if user is a doctor or a patient
    """
    return is_doctor(user) or is_patient(user)


def is_not_admin(user):
    """
    Helper function that checks if a user is a doctor or a patient
    :param user: The user to be checked
    :return: True if user is a doctor or a patient
    """
    return not is_admin(user)


@login_required
@user_passes_test(is_not_admin)
def appointment_main(request):
    """
    Appointment_main renders the main appointment page. It detects the user type (admin, patient, nurse, etc)
    and shows them the appropriate options

    :param request: The request with user information
    :return: The page to be rendered
    """
    parent = "core/landing/baselanding.html"

    if request.user.groups.filter(name='Patient').exists():
        appointments = Appointment.objects.filter(patient=request.user.patient).order_by('appointmentStart')
        return render(request, 'appointments/patientappointment.html', {'appointments': appointments, 'parent': parent})
    elif request.user.groups.filter(name='Doctor').exists():

        appointments = Appointment.objects.filter(doctor=request.user.doctor)
        return render(request, 'appointments/patientappointment.html', {'appointments': appointments, 'parent': parent})
    if request.user.groups.filter(name='Nurse').exists():

        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)

        appointments = Appointment.objects.filter(hospital=request.user.nurse.hospital,
                                                  appointmentStart__range=[start_week, end_week])

        return render(request, 'appointments/patientappointment.html', {'appointments': appointments, 'parent': parent})
    else:
        return HttpResponseForbidden()


@login_required
@user_passes_test(is_not_admin)
def CreateAppointment(request):
    """
     View to create an appointment. It ensures that the appointment is valid, and that there is not an appointment
     already at the time with the designated doctor

    :param request: The request with user information
    :return: The page to be rendered
    """
    created = False

    already_exists = False

    parent = get_parent(request)

    if request.method == 'POST':
        appointment_form = AppointmentForm(data=request.POST)

        if appointment_form.is_valid():

            appointment = appointment_form.save(commit=False)

            if Appointment.objects.filter(
                            Q(appointmentStart=appointment.appointmentStart) & Q(doctor=appointment.doctor)).exists():
                already_exists = True

            else:
                appointment_form.save()

                # Register Log
                log = Log.objects.create_Log(request.user, request.user.username, timezone.now(),
                                             "Appointment Created by " + request.user.username)
                log.save()

                created = True

        else:
            print("Error")
            print(appointment_form.errors)

    else:
        appointment_form = AppointmentForm()

    return render(request, "appointments/patientappointmentform.html",
                  {'appointment_form': appointment_form, 'registered': created, 'already_exists': already_exists,
                   'parent': parent})


class EditAppointment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    EditAppointment extends UpdateView, which is the generic class for editing preexisting objects
    This allows for a user to change their appointments

    """
    model = Appointment

    template_name = 'appointments/appointmentedit.html'

    form_class = AppointmentForm

    success_url = reverse_lazy('appointment_home')

    def test_func(self):
        return is_not_admin(self.request.user)


class DeleteAppointment(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    DeleteAppointment extends DeleteView, which is the generic class for deleting objects
    DeleteAppointment will delete the appointment, and is only visible to doctors and patients
    """
    model = Appointment

    success_url = reverse_lazy('appointment_home')

    template_name = 'appointments/appointmentdelete.html'

    def test_func(self):
        return is_not_admin(self.request.user)


def get_parent(request):
    """
    A helper method that returns the appropriate parent for the designated user type

    :param request: The request with user information
    :return: The parent that a template will extend
    """
    parent = 'core/landing/Patient.html'

    if request.user.groups.filter(name='Doctor').exists():
        parent = 'core/landing/Doctor.html'

    elif request.user.groups.filter(name='Nurse').exists():
        parent = 'core/landing/Nurse.html'

    elif request.user.groups.filter(name='Admin').exists():
        parent = 'core/landing/Admin.html'

    return parent
