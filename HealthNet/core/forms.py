from django.utils import timezone

from django import forms
from django.contrib.auth.models import User

from datetimewidget.widgets import DateWidget
from .models import Patient, Hospital, Doctor, Nurse


class UserRegForm(forms.ModelForm):
    """
    Form for user registration
    """
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserRegForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

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
    birthday = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    preferred_hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=False)
    # hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)
    emergency_contact = forms.EmailField(label="Emergency Contact Email Address:")

    class Meta:
        model = Patient
        fields = ('birthday', 'sex', 'blood_type', 'height', 'weight', 'allergies', 'medical_history', 'insurance_info',
                  'emergency_contact', 'preferred_hospital')  # , 'hospital')

    def __init__(self, *args, **kwargs):
        super(PatientRegForm, self).__init__(*args, **kwargs)

        self.fields['birthday'].widget.attrs.update({'class': 'form-control'})
        self.fields['sex'].widget.attrs.update({'class': 'form-control'})
        self.fields['blood_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['height'].widget.attrs.update({'class': 'form-control'})
        self.fields['weight'].widget.attrs.update({'class': 'form-control'})
        self.fields['allergies'].widget.attrs.update({'class': 'form-control'})
        self.fields['insurance_info'].widget.attrs.update({'class': 'form-control'})
        self.fields['emergency_contact'].widget.attrs.update({'class': 'form-control'})
        self.fields['preferred_hospital'].widget.attrs.update({'class': 'form-control'})
        self.fields['medical_history'].widget.attrs.update({'class': 'form-control'})
        # self.fields['hospital'].widget.attrs.update({'class': 'form-control'})


class NurseRegForm(forms.ModelForm):
    """
    Form for Nurse registration
    Note: Seperate from user registration form
    """
    now = timezone.now()
    phoneNum = forms.IntegerField(label="Phone Number")
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True, label="Hospital")

    class Meta:
        model = Nurse
        fields = ('phoneNum', 'hospital')


class DoctorRegForm(forms.ModelForm):
    """
    Form for Doctor registration
    Note: Seperate from user registration form
    """
    phoneNum = forms.IntegerField(label="Phone Number")
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True, label="Hospital")

    class Meta:
        model = Doctor
        fields = ('phoneNum', 'hospital')


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
        fields = ['birthday', 'sex', 'height', 'weight', 'allergies', 'medical_history', 'insurance_info',
                  'emergency_contact', 'preferred_hospital']


class PatientMediForm(forms.ModelForm):
    """
    Form for accessing Patient Medical Data
    """

    class Meta:
        model = Patient
        fields = ('sex', 'blood_type', 'height', 'weight', 'allergies', 'medical_history')


class UploadFileForm(forms.Form):
    """
    Form for Uploading Files
    """
    file = forms.FileField()


class NewHospitalForm(forms.ModelForm):
    """
    Form for creating a new Hospital
    """
    class Meta:
        model = Hospital
        fields = ('name',)
