from django import forms
from .models import Prescription, Patient
from django.utils import timezone


class PrescriptionForm(forms.ModelForm):

    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)
    date_prescribed = timezone.now()

    class Meta:
        model = Prescription
        fields = ('patient', 'drug', 'dosage', 'Dose_units', 'rate', 'Time_units')
