from core.models import Patient, Hospital, Doctor
from django import forms

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """
    AppointmentForm is the form for creating and editing appointments
    """
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)

    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=True)

    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)

    appointmentNotes = forms.CharField(widget=forms.Textarea, label="Notes")

    class Meta:
        model = Appointment

        fields = {'patient', 'doctor', 'hospital', 'appointmentStart', 'appointmentEnd', 'appointmentNotes'}
