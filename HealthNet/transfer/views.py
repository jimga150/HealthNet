from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone

from core.views import is_doctor, is_admin
from .models import Log
from .forms import TransferForm


def is_doctor_or_admin(user):
    """
    Helper function that tells if a user is of type Doctor or Admin
    :param user: user being checked for type
    :return: True if either Doctor or Admin, False otherwise
    """
    return is_doctor(user) or is_admin(user)


@login_required
@user_passes_test(is_doctor_or_admin)
def transfer_main(request):
    """
    Renders the main page for searching for a Patient in the system to transfer.
    :param request: user request for main page.
    :return: the page
    """

    transfer_form = TransferForm()

    return render(request, 'transfer/transfer_landing.html',  {'transfer_form': transfer_form})


@login_required
@user_passes_test(is_doctor_or_admin)
def create(request):
    """
    Creates a Transfer object for logging and performs transfer logic.
    :param request: the request from the transfer form
    :return: confirmation page
    """

    if request.method == 'POST':
        transfer_form = TransferForm(data=request.POST)
        if transfer_form.is_valid():
            transfer_form = TransferForm(data=request.POST)
            transfer = transfer_form.save()

            transfer.patient.hospital = transfer.New_Hospital
            transfer.patient.save()

            transfer_log = Log.objects.create_Log(request.user, transfer.patient.__str__(), timezone.now(), transfer.__str__())
            transfer_log.save()
            return render(request, 'transfer/transfer_confirmation.html')
    else:
        transfer_form = TransferForm
    # queryset = User.objects.all().exclude(pk=request.user.id)
    return render(request, 'transfer/transfer_landing.html',  {'transfer_form': transfer_form})


@login_required
@user_passes_test(is_doctor_or_admin)
def confirmation(request):
    """
    Returns confirmation page.
    """
    return render(request, 'transfer/transfer_confirmation.html')
