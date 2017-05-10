from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from core.views import is_patient, is_doctor
from .forms import ResultForm
from .models import Results
from core.models import Log, Patient
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def is_doctor_or_patient(user):
    """
    Checks if user logged in is of type doctor or patient
    :param user: user logged in
    :return: True if user is a doctor or patient
    """
    return is_doctor(user) or is_patient(user)


@login_required
@user_passes_test(is_doctor_or_patient)
def index(request):
    """
     displays the main page of the test results system
    :param request: Self explanatory
    :return: render containing the html page and all the tests for the user
    """

    results = Results.objects.order_by('date').reverse()

    return render(request, "results_main.html", {'results': results})


@login_required
@user_passes_test(is_doctor)
def createResult(request):
    """
        Creates a Test Result that can be released to a specific patient
        :param request: Self explanatory
        :return: render containing the html page and the info needed for the test result
        """
    if request.method == 'POST':
        results_form = ResultForm(request.POST, request.FILES)

        if results_form.is_valid():

            result = results_form.save(commit=False)

            result.doctor = request.user

            result.date = timezone.now()

            result.file = request.FILES['files']

            results_form.save()

            # Register Log
            log = Log.objects.create_Log(request.user, request.user.username, timezone.now(),
                                         request.user.username + " created Test Result")
            log.save()

            return HttpResponseRedirect(reverse_lazy('results_home'))
    else:
        results_form = ResultForm()

    return render(request, 'results_create.html', {'results_form' : results_form})


class UpdateTest(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows for edits to be made to the Test Result
    """

    model = Results

    template_name = 'results_edit.html'

    form_class = ResultForm

    success_url = reverse_lazy('results_home')

    def test_func(self):
        return is_doctor(self.request.user)


class DeleteTest(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows for the test result to be deleted
    """

    model = Results

    template_name = 'results_delete.html'

    success_url = reverse_lazy('results_home')

    def test_func(self):
        return is_doctor(self.request.user)


@login_required
@user_passes_test(is_patient)
def view_for_patient(request):
    """
    Display specifically for patients as to make sure they can't create tests themselves
    :param request: Self explanatory
    :return: render containing the html page and all the tests for the patient
    """

    patient = Patient.objects.all().get(user=request.user)

    results = Results.objects.all().filter(patient=patient).filter(released=True).order_by('date').reverse()
    print(str(results))

    return render(request, "results_main.html", {'results': results})
