from django.shortcuts import render
from .forms import ResultForm
from .models import Results
from core.models import Log, Patient
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):

    results = Results.objects.order_by('date').reverse()

    return render(request, "results_main.html", {'results' : results})


def createResult(request):

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


class UpdateTest(LoginRequiredMixin, UpdateView):

    model = Results

    template_name = 'results_edit.html'

    form_class = ResultForm

    success_url = reverse_lazy('results_home')


class DeleteTest(LoginRequiredMixin, DeleteView):

    model = Results

    template_name = 'results_delete.html'

    success_url = reverse_lazy('results_home')


def view_for_patient(request, patient_id):

    results = Results.objects.filter(patient=Patient.objects.get(pk=patient_id)).order_by('date').reverse()

    return render(request, "results_main.html", {'results': results})
