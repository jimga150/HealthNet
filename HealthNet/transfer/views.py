from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from core.views import is_doctor, is_admin
from .models import Transfer, Log
from .forms import TransferForm


def is_doctor_or_admin(user):
    """
    Helper function that tells if a user is of type Doctor or Admin
    :param user: user being checked for type
    :return: True if either Doctor or Admin, False otherwise
    """
    if is_doctor(user) | is_admin(user):
        return True
    else:
        return False


@login_required
@user_passes_test(is_doctor_or_admin)
def transfer_main(request):
    """
    Renders the main page for searching for a Patient in the system to transfer.
    :param request: user request for main page.
    :return: the page
    """

    transfer_form = TransferForm()

    return render(request, 'transfer/transfer_landing.html',  {'transfer_form' : transfer_form})


# Create your views here.
def create(request):
    """
    Creates a Transfer object for logging and performs transfer logic.
    :param request: the request from the transfer form
    :return: confirmation page
    """
    transfer_form = TransferForm(data=request.POST)
    transfer = transfer_form.save()

    transfer.patient.preferred_hospital = transfer.newHospital
    transfer.save()

    transfer_log = Log.objects.create_Log(request.user, transfer.patient.__str__(), timezone.now(), transfer.__str__())
    transfer_log.save()

    return render(request, 'transfer/transfer_confirmation.html')


def confirmation(request):
    """
    Returns confirmation page.
    """
    return render(request, 'transfer/transfer_confirmation.html' )