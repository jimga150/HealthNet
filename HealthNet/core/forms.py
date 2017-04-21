from django.utils import timezone

from django import forms
from django.contrib.auth.models import User

from .models import Patient, Hospital, Doctor, Nurse


class UserRegForm(forms.ModelForm):
    """
    Form for user registration
    """
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def is_valid(self):
        return super(UserRegForm, self).is_valid() and \
               User.objects.all().filter(email=self.cleaned_data['email']).count() == 0


class UserUpdateForm(forms.ModelForm):
    """
    Form for user updates
    """

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class PatientRegForm(forms.ModelForm):
    """
    Form for patient registration
    Note: Seperate from user registration form
    """
    now = timezone.now()
    birthday = forms.DateField()
    preferred_hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=False)
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)

    class Meta:
        model = Patient
        fields = (
            'birthday', 'sex', 'blood_type', 'height', 'weight', 'allergies', 'insurance_info', 'emergency_contact',
            'preferred_hospital', 'hospital')


class NurseRegForm(forms.ModelForm):
    """
    Form for patient registration
    Note: Seperate from user registration form
    """
    now = timezone.now()
    phoneNum = forms.IntegerField(label="Phone Number")
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=False, label="Hospital")

    class Meta:
        model = Nurse
        fields = (
            'phoneNum', 'hospital')


class DoctorRegForm(forms.ModelForm):
    """
    Form for patient registration
    Note: Seperate from user registration form
    """
    phoneNum = forms.IntegerField(label="Phone Number")

    class Meta:
        model = Doctor
        fields = (
            'phoneNum',)


class LoginForm(forms.ModelForm):
    """
    Form for logging in
    """

    class Meta:
        model = User
        username = forms.CharField(max_length=50)
        password = forms.CharField(max_length=50)
        fields = ["username", "password"]


class PatientForm(forms.ModelForm):
    """
    Form for accessing Patient Data
    """

    class Meta:
        model = Patient
        fields = ['birthday', 'sex', 'blood_type', 'height', 'weight', 'allergies', 'insurance_info',
                  'emergency_contact', 'preferred_hospital', 'hospital']


class PatientMediForm(forms.ModelForm):
    """
    Form for accessing Patient Medical Data
    """

    class Meta:
        model = Patient
        fields = (
            'birthday', 'sex', 'blood_type', 'height', 'weight', 'allergies', 'insurance_info', 'emergency_contact',
            'preferred_hospital', 'hospital')


class UploadFileForm(forms.Form):
    """
    Form for Uploading Files
    """
    file = forms.FileField()
