from django import forms
from .models import Results
from core.models import Patient


class ResultForm(forms.ModelForm):
    """
    Form that displays and gets the information from the user for the test result
    """
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)
    name = forms.CharField(max_length=100, required=True)
    files = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
        required=True
    )
    notes = forms.CharField(max_length=500, required=False)
    released = forms.BooleanField(required=False)

    class Meta:
        model = Results

        fields = {'name', 'notes', 'patient', 'released', 'files'}