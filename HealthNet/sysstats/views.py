from django.shortcuts import render
from .forms import DateFilterForm

from core.models import *
from messaging.models import *
from prescriptions.models import *
from testResults.models import *
from transfer.models import *

from django.contrib.auth.decorators import login_required, user_passes_test
from core.views import is_admin

from django.utils import timezone


@login_required
@user_passes_test(is_admin)
def stats(request):
    """
    Compiles several tables worth of statistics on the site and passes it into a premade template as context. Allows
    POST requests to be made, filtering data (that is able to be filtered) by a start and end date. Loading from no POST
    results in no time filtering.
    :param request: The request with possible date filtering parameters
    :return: Rendered template, complete with useful stats context.
    """
    if request.method == 'POST':

        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = str(form.cleaned_data['start_date'])
            end_date = str(form.cleaned_data['end_date'])

            if len(start_date) < 10:
                startDate = timezone.datetime(1970, 1, 1)
            else:
                start_year = int(start_date[:4])
                start_month = int(start_date[5:7])
                start_day = int(start_date[8:])
                startDate = timezone.datetime(start_year, start_month, start_day)

            if len(end_date) < 10:
                endDate = timezone.now()
            else:
                end_year = int(end_date[:4])
                end_month = int(end_date[5:7])
                end_day = int(end_date[8:])
                endDate = timezone.datetime(end_year, end_month, end_day)
        else:
            form = DateFilterForm()
            startDate = timezone.datetime(1970, 1, 1)
            endDate = timezone.now()
    else:
        form = DateFilterForm()
        startDate = timezone.datetime(1970, 1, 1)
        endDate = timezone.now()

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    nurses = Nurse.objects.all()
    admins = Admin.objects.all()
    labels = ["Doctors", "Nurses", "Patients", "Admins"]
    counts = [doctors.count(), nurses.count(), patients.count(), admins.count()]

    logs = Log.objects.all()
    logins = logs.filter(type__contains=" logged in").filter(time__range=[startDate, endDate])
    logouts = logs.filter(type__contains=" logged out").filter(time__range=[startDate, endDate])
    registrations = logs.filter(type__contains="Patient Registered").filter(time__range=[startDate, endDate])
    appointments = logs.filter(type__contains="Appointment Created by ").filter(time__range=[startDate, endDate])
    transfers = logs.filter(type__contains="was transferred to").filter(time__range=[startDate, endDate])
    info_views = logs.filter(type__contains="Medical Info viewed").filter(time__range=[startDate, endDate])
    info_edits = logs.filter(type__contains="Medical Info updated").filter(time__range=[startDate, endDate])

    loglabels = ["Logins", "Logouts", "Registrations", "Apppointment creations", "Transfers",
                 "Medical Info Views", "Medical Info Edits"]
    logcounts = [logins.count(), logouts.count(), registrations.count(), appointments.count(), transfers.count(),
                 info_views.count(), info_edits.count()]

    messages = Message.objects.all().filter(date__range=[startDate, endDate])
    m_labels = ["Date", "Sender", "Recipient", "Subject"]
    dates = []
    senders = []
    recipients = []
    subjects = []
    for m in messages.iterator():
        dates.append(m.date)
        senders.append(m.sender)
        recipients.append(m.recipient)
        subjects.append(m.subject)

    m_list = zip(dates, senders, recipients, subjects)

    prescriptions = Prescription.objects.all().filter(date_prescribed__range=[startDate, endDate])
    p_labels = ["Patient", "Doctor", "Drug"]
    patients = []
    doctors = []
    drugs = []
    for p in prescriptions.iterator():
        patients.append(p.patient)
        doctors.append(p.doctor)
        drugs.append(p.drug)

    p_list = zip(patients, doctors, drugs)

    test_results = Results.objects.all().filter(date__range=[startDate, endDate])
    tr_labels = ["Name", "Patient", "Doctor", "Released"]
    names = []
    patients = []
    doctors = []
    released = []
    for tr in test_results.iterator():
        names.append(tr.name)
        patients.append(tr.patient)
        doctors.append(tr.doctor)
        released.append(tr.released)

    tr_list = zip(names, patients, doctors, released)

    context = {'Users': zip(labels, counts), 'Logs': zip(loglabels, logcounts), 'Message_count': messages.count(),
               'Message_labels': m_labels, 'Messages': m_list, 'Prescription_count': prescriptions.count(),
               'Prescription_labels': p_labels, 'Prescriptions': p_list, 'tr_count': test_results.count(),
               'Test_result_labels': tr_labels, 'Test_results': tr_list, 'form': form,
               "StartDate": str(startDate).replace("-", "/")[:10], "EndDate": str(endDate).replace("-", "/")[:10]}

    return render(request, "sysstats/viewstats.html", context)
