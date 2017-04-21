""""""
from django.utils import timezone

from django import forms
from django.contrib.auth.models import User

from .models import Patient, Hospital, Transfer

class TransferForm(forms.ModelForm):
    """
    Look up Patient and Hospital to transfer to.
    """

    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)
    newHospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)

    class Meta:
        model = Transfer
        fields = { 'patient', 'newHospital' }