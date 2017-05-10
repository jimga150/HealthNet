from django.shortcuts import redirect

from .forms import PrescriptionForm

from core.views import is_doctor, is_nurse, is_admin, is_patient

from core.models import *
from .models import Prescription

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.shortcuts import render
from django.core.urlresolvers import reverse


def not_admin(user):
    """
    :param user: The User in question
    :return: True if the user is anything but an Admin
    """
    return not is_admin(user)


def is_doctor_or_nurse(user):
    """
    :param user: The User in question
    :return: True if the user is a Doctor or Nurse
    """
    return is_doctor(user) or is_nurse(user)


@login_required
@user_passes_test(is_doctor)
def new_prescription(request):
    """
    Page for the form a doctor fills out to prescribe a drug
    :param request: the request with possible form submission
    :return: Prescription form or redirect to listing page (below)
    """
    if request.method == 'POST':

        prescription_form = PrescriptionForm(data=request.POST)

        validity = prescription_form.is_valid()
        if validity:

            prescription = prescription_form.save(commit=False)
            prescription.date_prescribed = timezone.now()
            prescription.doctor = Doctor.objects.all().get(user=request.user)
            prescription.save()

            log = Log.objects.create_Log(request.user, request.user.username, timezone.now(),
                                         "Prescription filled out")
            log.save()
        else:
            print("Error")
            print(prescription_form.errors)
        if 'submit_singular' in request.POST and validity:
            return redirect('prescriptions')
        elif 'submit_another' in request.POST:
            prescription_form = PrescriptionForm()
    else:
        prescription_form = PrescriptionForm()

    context = {"prescription_form": prescription_form}
    return render(request, 'prescriptions/makenew.html', context)


def get_prescription_list_for(cpatient):
    """
    Generic getter for a specific patient's prescription list
    :param cpatient: Patient to fetch list for
    :return: context of Prescription list
    """
    Prescriptions = Prescription.objects.all().filter(patient=cpatient)
    per = []
    for p in Prescriptions.iterator():
        per.append(str(dict(p.TIME_CHOICES)[p.Time_units]))
    p_list = zip(Prescriptions, per)
    return {"Labels": ["Doctor", "Drug", "Dosage", "Rate"], "Name": str(cpatient), "Prescriptions": p_list}


@login_required
@user_passes_test(not_admin)
def prescriptions(request):
    """
    Lists either all patients in the hospital with links to their prescription lists, or the prescriptions applied to a
    single defined patient. 
    :param request: The request sent in, not used here
    :return: List page rendering
    """

    context = {}

    if is_doctor(request.user) or is_nurse(request.user):

        context["Labels"] = ["Name", "Prescriptions"]

        patients = Patient.objects.all()
        prescription_nums = []
        for pat in patients.iterator():
            prescription_nums.append(Prescription.objects.filter(patient=pat).count())
        context["Patients"] = zip(patients, prescription_nums)

    elif is_patient(request.user):
        cpatient = Patient.objects.get(user=request.user)
        context = get_prescription_list_for(cpatient)
        context["is_doctor"] = is_doctor(request.user)

    context["is_doctor"] = is_doctor(request.user)

    return render(request, 'prescriptions/list.html', context)


@login_required
@user_passes_test(is_doctor_or_nurse)
def prescriptions_list(request, patient_id):
    """
    Page that doctors and nurses are sent to when accessing a single patient's prescription list.
    :param request: The request sent in, not used here
    :param patient_id: ID of the patient who's being listed
    :return: List page rendering
    """
    cpatient = Patient.objects.get(pk=patient_id)
    context = get_prescription_list_for(cpatient)
    context["is_doctor"] = is_doctor(request.user)

    return render(request, 'prescriptions/list.html', context)


@login_required
@user_passes_test(is_doctor)
def delete_prescription(request, prescription_id):
    """
    Page for confirming/deleting a single prescription
    :param request: The request sent in, not used here
    :param prescription_id: ID number of the prescription in question
    :return: Redirect or confirmation page
    """
    prescription = Prescription.objects.get(pk=prescription_id)
    patient_id = prescription.patient.id

    if request.method == 'POST':
        prescription.delete()
        return redirect(reverse('list prescriptions for patient', kwargs={'patient_id': patient_id}))

    context = {"Prescription": prescription, 'patient_id': patient_id}

    return render(request, 'prescriptions/delete.html', context)
