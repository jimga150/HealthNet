from django import forms
from .models import Patient, Hospital, Transfer


class TransferForm(forms.ModelForm):
    """
    Look up Patient and Hospital to transfer to.
    """

    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)
    New_Hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)

    class Meta:
        model = Transfer
        fields = {'patient', 'New_Hospital'}
