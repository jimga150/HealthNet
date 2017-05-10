from io import TextIOWrapper

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import UpdateView, CreateView, DetailView

from prescriptions.models import Prescription
from .forms import *
from .models import *


def is_patient(user):
    """
    Helper function that checks if a user is a patient
    :param user: The user to be checked
    :return: True if user is a patient
    """
    if user:
        return user.groups.filter(name='Patient').count() != 0
    return False


def is_doctor(user):
    """
    Helper function that checks if a user is a doctor
    :param user: The user to be checked
    :return: True if user is a doctor
    """
    if user:
        return user.groups.filter(name='Doctor').count() != 0
    return False


def is_nurse(user):
    """
    Helper function that checks if a user is a nurse
    :param user: The user to be checked
    :return: True if user is a nurse
    """
    if user:
        return user.groups.filter(name='Nurse').count() != 0
    return False


def is_doctor_or_nurse(user):
    """
    Uses above functions combined to fit the @user_passes_test mixin
    :param user: The User in question
    :return: True if the user is a Doctor or Nurse
    """
    return is_doctor(user) or is_nurse(user)


def not_patient(user):
    """
    Users is_patient funtion to test if user is of patient type
    :param user: The User in question
    :return: True if user is not a patient
    """
    return not is_patient(user)


def is_admin(user):
    """
    Helper function that checks if a user is an admin
    :param user: The user to be checked
    :return: True if user is an admin
    """
    if user:
        return user.groups.filter(name='Admin').count() != 0
    return False


def user_login(request):
    """
    Renders the user login page, and redirects the user to the appropriate landing page

    :param request: The request with user information
    :return: The page to be rendered
    """
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:

                login(request, user)

                # Register Log
                log = Log.objects.create_Log(user, user.username, timezone.now(), user.username + " logged in")
                log.save()

                return HttpResponseRedirect(reverse('landing'))

            else:
                return HttpResponse("Your Account has been Deactivated")
        else:
            print("Invalid login: {0}".format(username))
            context = RequestContext(request)
            context['login_failure'] = True
            return render(request, 'core/login.html', context)

    else:
        return render(request, 'core/login.html', RequestContext(request))


@login_required
def user_logout(request):
    """
    Logs out a user, and logs it

    :param request: The request with user information
    :return: The page to be rendered
    """
    # Register Log
    log = Log.objects.create_Log(request.user, request.user.username, timezone.now(),
                                 request.user.username + " logged out")
    log.save()

    logout(request)

    return HttpResponseRedirect(reverse('login'))


@login_required
@user_passes_test(is_patient)
def patient_landing(request):
    """
    Renders the patient landing page

    :param request: The request with user information
    :return: The page to be rendered
    """
    return render(request, 'core/landing/Patient.html')


@login_required
def profile(request):
    """
    Displays the user Profile Information

    :param request: The request with user information
    :return: The page to be rendered
    """

    parent = get_parent(request)

    return render(request, 'core/landing/pages/profile.html', {'parent': parent})


def QueryListtoString(query):
    """
    Used to convert Query lists to readable strings, used in the following Medical Information Export function.
    :param query: the query to convert
    :return: the readable string
    """
    ans = ""
    for q in query.iterator():
        ans = ans + str(q) + '\n'
    return ans


def MediInfoExport(Patient_exporting: Patient, assoc_user: User, is_email):
    """
    Generic getter for a patient's complete medical information into a readable format in a String
    :param Patient_exporting: The Patient exporting their info
    :param assoc_user: The Patient's associated User
    :param is_email: True if this is being sent in an email (adds greeting), false otherwise
    :return: The complete text export
    """
    Name = 'Name: ' + str(assoc_user.get_full_name())
    Email = 'Email: ' + str(assoc_user.email)
    Birthday = 'Birthday: ' + str(Patient_exporting.birthday)
    Gender = 'Sex: ' + str(dict(Patient_exporting.SEX_CHOICE)[Patient_exporting.sex])
    Blood_Type = 'Blood-Type: ' + str(dict(Patient_exporting.BLOOD_TYPE)[Patient_exporting.blood_type])
    Height = 'Height: ' + str(Patient_exporting.height)
    Weight = 'Weight: ' + str(Patient_exporting.weight) + ' lbs'

    Allergies = 'Allergies: \r\n' + str(Patient_exporting.allergies)

    Medical_History = 'Medical-History: \r\n' + str(Patient_exporting.medical_history)

    Prescriptions = 'Prescriptions: \r\n' + \
                    str(QueryListtoString(Prescription.objects.all().filter(patient=Patient_exporting)))

    Insurance_Info = 'Insurance-Info: ' + str(Patient_exporting.insurance_info)
    Preferred_Hospital = 'Preferred-Hospital: ' + str(Patient_exporting.preferred_hospital)
    PHospital = 'Current-Hospital: ' + str(Patient_exporting.hospital)
    Emergency_Contact = 'Emergency-Contact: ' + str(Patient_exporting.emergency_contact)

    ans = Name + '\r\n' + \
          Email + '\r\n' + \
          Birthday + '\r\n' + \
          Gender + '\r\n' + \
          Blood_Type + '\r\n' + \
          Height + '\r\n' + \
          Weight + '\r\n\r\n' + \
          Allergies + '\r\n\r\n' + \
          Medical_History + '\r\n\r\n' + \
          Prescriptions + '\r\n\r\n' + \
          Insurance_Info + '\r\n' + \
          Preferred_Hospital + '\r\n' + \
          PHospital + '\r\n' + \
          Emergency_Contact + '\r\n'

    if is_email:
        return 'Hello ' + str(assoc_user.first_name) + \
               ', \n\n\tYou are receiving this email as an export of your medical information from ' + \
               str(Patient_exporting.hospital) + '. Below you\'ll find the medical record export. ' \
                                                 'Thank you for using HealthNet!\n\n' + ans
    return ans


@login_required
@user_passes_test(is_patient)
def email(request):
    """
    Sends the patient an email with a full summary of their medical information.

    :param request: The request with user information
    :return: The success landing page
    """
    Pat = Patient.objects.all().get(user=request.user)

    if request.user.email_user('Medical Information Export: ' + request.user.get_full_name(),
                               MediInfoExport(Pat, request.user, True),
                               'DjangoTeam4Bot@gmail.com',
                               fail_silently=True,
                               ):
        return render(request, 'core/landing/pages/email_success.html')
    else:
        return render(request, 'core/landing/pages/profile.html', {'parent': get_parent(request)})


@login_required
@user_passes_test(is_patient)
def download(request):
    """
    Serves patients full summary as a downloadable text file.

    :param request: The request with user information
    :return: Downloadable text file, in lieu of a conventional response
    """
    Pat = Patient.objects.all().get(user=request.user)

    content = MediInfoExport(Pat, request.user, False)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s_Info.txt"' % \
                                      str(request.user.get_full_name()).replace(' ', '-')
    return response


def listtostring(listin):
    """
    Converts a simple list into a space separated sentence, effectively reversing str.split(" ")
    :param listin: the list to convert
    :return: the readable string
    """
    ans = ""
    for l in listin:
        ans = ans + str(l) + " "
    return ans.strip()


def read_new_Patient(filename, encoding, doctor_user):
    """
    Reads in a new Patient from the specific file, assumes that the patient instance already exists and is associated
    with an existing user, but not necessarily populated.
    :param doctor_user: User of Doctor signing off on Patient import, used when constructing Prescriptions
    :param filename: Name of the file to read from
    :param encoding: UTF-8, ANSI, etc etc
    :return: The newly populated Patient class (after its been saved)
    """
    # print("reading new patient...")
    file = TextIOWrapper(filename.file, encoding=encoding)

    new_patient = None
    Allergies_mode = False
    Prescriptions_mode = False
    Medical_History_mode = False
    Allergies = ''
    Medical_History = ''
    Prescriptions = []

    for line in file.readlines():
        print("Line: " + line)
        words = line.strip().split(" ")
        print(words)
        instance_var = words[0]
        # print("Current variable is " + instance_var)
        if Allergies_mode:
            if line.strip() != '':
                # print('found allergy: ' + line.strip())
                Allergies = Allergies + line.strip()
            else:
                # print('And that\'s it for allergies')
                Allergies_mode = False
                new_patient.allergies = Allergies
        elif Medical_History_mode:
            if line.strip() != '':
                # print('found medical history: ' + line.strip())
                Medical_History = Medical_History + line.strip()
            else:
                # print('And that\'s it for medical history')
                Medical_History_mode = False
                new_patient.medical_history = Medical_History
        elif Prescriptions_mode:
            if line.strip() != '':
                # print('found prescription: ' + line.strip())
                Prescriptions.append(line.strip())
            else:
                # print('And that\'s it for prescriptions')
                Prescriptions_mode = False
                for p in Prescriptions:
                    Prescription.fromString(p, new_patient.id, doctor_user)
        if instance_var == 'Email:':
            Email = words[1]
            print("found email: " + Email)
            user = User.objects.get(email=Email)
            new_patient = Patient.objects.get(user=user)
            print(new_patient)
        elif instance_var == 'Birthday:':
            print("found b-day: " + words[1])
            new_patient.birthday = words[1]
        elif instance_var == 'Sex:':
            print("found sex: " + words[1])
            new_patient.sex = words[1]
        elif instance_var == 'Blood-Type:':
            print("found b-type: " + words[1])
            new_patient.blood_type = words[1]
        elif instance_var == 'Height:':
            print("found height: " + words[1])
            new_patient.height = words[1]
        elif instance_var == 'Weight:':
            print("found weight: " + words[1])
            new_patient.weight = words[1]
        elif instance_var == 'Allergies:':
            print("found Allergies")
            Allergies_mode = True
        elif instance_var == 'Medical-History::':
            print("found Medical History")
            Medical_History_mode = True
        elif instance_var == 'Prescriptions:':
            print("found prescriptions")
            Prescriptions_mode = True
        elif instance_var == 'Insurance-Info:':
            insurance = listtostring(words[1:])
            print("found Insurance: " + insurance)
            new_patient.insurance_info = insurance
        elif instance_var == 'Preferred-Hospital:':
            p_hospital = listtostring(words[1:])
            print("found hospital: " + p_hospital)
            new_patient.preferred_hospital = Hospital.objects.get(name=p_hospital)
        elif instance_var == 'Emergency-Contact:':
            print("found e-contact: " + words[1])
            new_patient.emergency_contact = words[1]
            # elif instance_var == 'Current-Hospital:':
            #     c_hospital = listtostring(words[1:])
            #     print("found hospital: " + c_hospital)
            #     new_patient.hospital = Hospital.objects.get(name=c_hospital)
    return new_patient.save()


@login_required
@user_passes_test(is_doctor_or_nurse)
def upload_patient_info(request):
    """
    View for uploading a text file with pateint information
    :param request: request with possible file upload
    :return: the current page again with possible confirmation
    """
    uploaded = False

    if request.method == 'POST':
        attempted = True
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            read_new_Patient(request.FILES['file'], request.encoding, request.user)
            uploaded = True
        else:
            uploaded = False
    else:
        attempted = False
        form = UploadFileForm()
    return render(request, 'core/upload_patient.html', {'form': form, 'attempted': attempted,
                                                        'upload_success': uploaded})


@login_required
@user_passes_test(is_nurse)
def nurse_landing(request):
    """
    Renders the patient landing page

    :param request: The request with user information
    :return: The page to be rendered
    """
    return render(request, 'core/landing/Nurse.html')


@login_required
@user_passes_test(is_doctor)
def doctor_landing(request):
    """
    Renders the doctor landing page

    :param request: The request with user information
    :return: The page to be rendered
    """
    return render(request, 'core/landing/Doctor.html')


@login_required
@user_passes_test(is_admin)
def admin_landing(request):
    """
    Renders the admin landing page

    :param request: The request with user information
    :return: The page to be rendered
    """
    return render(request, 'core/landing/Admin.html')


@login_required
@user_passes_test(is_admin)
def registerStaff(request):
    """
    Renders the registration selection page
    :param request: The request with user information
    :return: The page to be rendered
    """
    return render(request, 'core/landing/pages/registration_select.html')


@login_required
@user_passes_test(is_admin)
def register_nurse_page(request):
    """
    Registers a nurse as well as it's one-to-one user. Error checks fields, and ensures that all data is valid before
    creation

    :param request: The request with user information
    :return: The page to be rendered
    """
    registered = False

    if request.method == 'POST':
        user_form = UserRegForm(data=request.POST)
        other_form = NurseRegForm(data=request.POST)

        if user_form.is_valid() and other_form.is_valid():

            group = Group.objects.get(name='Nurse')

            user = user_form.save()
            if User.objects.all().filter(email=user.email).count() > 0:
                # throw an error, this became an issue
                pass
            user.set_password(user.password)
            user.groups.add(group)

            user.save()

            nprofile = other_form.save(commit=False)
            nprofile.user = user
            nprofile.save()

            # Register Log
            log = Log.objects.create_Log(nprofile.user, nprofile.user.username, timezone.now(), "Nurse Registered")
            log.save()

            registered = True

            # else:
            # print("Error")
            # print(user_form.errors, other_form.errors)

    else:
        user_form = UserRegForm()
        other_form = NurseRegForm()

    return render(request, "core/landing/pages/registrationPages/staff_registration.html",
                  {'user_form': user_form, 'other_form': other_form, 'registered': registered, 'stafftype': "nurse"})


@login_required
@user_passes_test(is_admin)
def register_doctor_page(request):
    """
    Registers a doctor as well as it's one-to-one user. Error checks fields, and ensures that all data is valid before
    creation

    :param request: The request with user information
    :return: The page to be rendered
    """
    registered = False

    if request.method == 'POST':
        user_form = UserRegForm(data=request.POST)
        other_form = DoctorRegForm(data=request.POST)

        if user_form.is_valid() and other_form.is_valid():

            group = Group.objects.get(name='Doctor')

            user = user_form.save()
            if User.objects.all().filter(email=user.email).count() > 0:
                # throw an error, this became an issue
                pass
            user.set_password(user.password)
            user.groups.add(group)

            user.save()

            dprofile = other_form.save(commit=False)
            dprofile.user = user
            dprofile.save()

            # Register Log
            log = Log.objects.create_Log(dprofile.user, dprofile.user.username, timezone.now(), "Doctor Registered")
            log.save()

            registered = True

            # else:
            # print("Error")
            # print(user_form.errors, other_form.errors)

    else:
        user_form = UserRegForm()
        other_form = DoctorRegForm()

    return render(request, "core/landing/pages/registrationPages/staff_registration.html",
                  {'user_form': user_form, 'other_form': other_form, 'registered': registered, 'stafftype': "doctor"})


@login_required
@user_passes_test(is_admin)
def register_admin_page(request):
    """
    Registers a admin as well as it's one-to-one user. Error checks fields, and ensures that all data is valid before
    creation

    :param request: The request with user information
    :return: The page to be rendered
    """
    registered = False

    if request.method == 'POST':
        user_form = UserRegForm(data=request.POST)

        if user_form.is_valid():

            group = Group.objects.get(name='Admin')

            user = user_form.save()
            if User.objects.all().filter(email=user.email).count() > 0:
                # throw an error, this became an issue
                pass
            user.set_password(user.password)
            user.groups.add(group)

            user.save()

            sadmin = Admin.objects.create(user=user)
            sadmin.save()

            # Register Log
            log = Log.objects.create_Log(sadmin.user, sadmin.user.username, timezone.now(), "Admin Registered")
            log.save()

            registered = True

            # else:
            #     print("Error")
            #     print(user_form.errors)

    else:
        user_form = UserRegForm()

    return render(request, "core/landing/pages/registrationPages/admin_registration.html",
                  {'user_form': user_form, 'registered': registered, 'stafftype': "admin"})


@login_required
def landing(request):
    """
    Renders the landing page

    :param request: The request with user information
    :return: The page to be rendered
    """
    context = {}
    parent = get_parent(request)
    if 'Patient' in parent:
        context['Patient_ID'] = Patient.objects.all().get(user=request.user).id
        print("Patient! id is " + str(context['Patient_ID']))

    return render(request, 'core/landing/baselanding.html', context)


def register_patient_page(request):
    """
    Registers a patient as well as it's one-to-one user. Error checks fields, and ensures that all data is valid before
    creation

    :param request: The request with user information
    :return: The page to be rendered
    """
    registered = False
    context = {}

    if request.method == 'POST':
        user_form = UserRegForm(data=request.POST)
        patient_form = PatientRegForm(data=request.POST)

        if user_form.is_valid() and patient_form.is_valid():

            group = Group.objects.get(name='Patient')

            user = user_form.save()

            user.set_password(user.password)
            user.groups.add(group)

            user.save()

            pprofile = patient_form.save(commit=False)
            pprofile.user = user
            if User.objects.filter(email=pprofile.emergency_contact).exists():
                pprofile.emergency_contact_user = User.objects.get(email=pprofile.emergency_contact)

            pprofile.hospital = pprofile.preferred_hospital

            pprofile.save()

            # Register Log
            log = Log.objects.create_Log(pprofile.user, pprofile.user.username, timezone.now(), "Patient Registered")
            log.save()

            registered = True

        else:
            print("Error")
            print(user_form.errors, patient_form.errors)

    else:
        user_form = UserRegForm()
        patient_form = PatientRegForm()

    context['user_form'] = user_form
    context['patient_form'] = patient_form
    context['registered'] = registered
    return render(request, "core/registerpatient.html", context)


def main(request):
    """
    Renders the main page

    :param request: The request with user information
    :return: The page to be rendered
    """
    # return render(request, 'core/main/base.html')
    return render(request, 'core/main/homepage.html')


@login_required
def patient_tests(request):
    """
    Renders the patient test page, nto yet implemented

    :param request: The request with user information
    :return: The page to be rendered
    """
    return redirect(reverse('results_home'))


@login_required
def editownprofile(request):
    """
    Allows user to update their profile information, plus certain User info
    :param request: The request with possible form info
    :return: The Edit page
    """
    parent = get_parent(request)

    person = None

    if 'Patient' in parent:
        person = Patient.objects.get(user=request.user)
    elif 'Doctor' in parent:
        person = Doctor.objects.get(user=request.user)
    elif 'Nurse' in parent:
        person = Nurse.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=request.user)

        person_form = None
        if 'Patient' in parent:
            person_form = PatientForm(data=request.POST, instance=person)
        elif 'Doctor' in parent:
            person_form = DoctorRegForm(data=request.POST, instance=person)
        elif 'Nurse' in parent:
            person_form = NurseRegForm(data=request.POST, instance=person)

        if user_form.is_valid():

            user = user_form.save()

            if person_form is not None and person_form.is_valid():
                pprofile = person_form.save(commit=False)
                pprofile.user = user

                if person is Patient and User.objects.filter(email=pprofile.emergency_contact).exists():
                    pprofile.emergency_contact_user = User.objects.get(email=pprofile.emergency_contact)

                pprofile.save()

            log = Log.objects.create_Log(request.user, request.user.username, timezone.now(),
                                         "User updated own info")
            log.save()

        else:
            # print("Error")
            # print(user_form.errors, person_form.errors)
            pass

        return render(request, 'core/landing/pages/profile.html', {'parent': parent})

    else:
        user_form = UserUpdateForm(instance=request.user)

        person_form = None
        if 'Patient' in parent:
            person_form = PatientForm(instance=person)
        elif 'Doctor' in parent:
            person_form = DoctorRegForm(instance=person)
        elif 'Nurse' in parent:
            person_form = NurseRegForm(instance=person)

        return render(request, 'core/landing/pages/edit_profile.html',
                      {'user_form': user_form, 'patient_form': person_form})


class EditPatientMediInfo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    EditPatientMediInfo extends UpdateView, which is the generic class for editing preexisting objects
    This allows for a user to change their information

    """
    model = Patient

    template_name = 'core/edit_medi_info.html'

    form_class = PatientMediForm

    def get_object(self, queryset=None):
        p_id = self.kwargs['patient_id']
        patient = Patient.objects.get(pk=p_id)
        log = Log.objects.create_Log(self.request.user, self.request.user.username, timezone.now(), "Patient(\"" +
                                     patient.user.get_full_name() + "\", id " + p_id + ") Medical Info updated")
        log.save()
        return patient

    def test_func(self):
        return is_doctor(self.request.user)


@login_required
@user_passes_test(not_patient)
def view_patients(request):
    """
    Simple view for fetching all the patients in the system onto a list and viewing them by name
    :param request: The request
    :return: rendered list page with patient context
    """
    labels = ["Name", "Email", "Birthday", "Hospital", "Admission Status"]

    context = {"Patients": Patient.objects.all(), "Labels": labels}
    return render(request, 'core/view_patients.html', context)


@login_required
@user_passes_test(is_admin)
def logs(request):
    """
    Shows all log objects

    :param request: The request with user information
    :return: The page to be rendered
    """
    Logs = Log.objects.order_by('time').reverse()
    return render(request, 'core/logs.html', {'logs': Logs})


def get_parent(request):
    """
    A helper method that returns the appropriate parent for the designated user type

    :param request: The request with user information
    :return: The parent that a template will extend
    """
    parent = 'core/landing/Patient.html'

    if request.user.groups.filter(name='Doctor').exists():
        parent = 'core/landing/Doctor.html'

    elif request.user.groups.filter(name='Nurse').exists():
        parent = 'core/landing/Nurse.html'

    elif request.user.groups.filter(name='Admin').exists():
        parent = 'core/landing/Admin.html'

    return parent


def swag(request):
    return render(request, 'core/landing/pages/registrationPages/swag.html')


@login_required
@user_passes_test(is_doctor_or_nurse)
def admitPatient(request, patient_id):
    """
    Allows Doctors and Nurses to admnit existing Patients
    :param request: self explanatory
    :param patient_id: ID number of the Patient to admit
    :return: view_patients list, after Patient has been admitted
    """
    patient = Patient.objects.get(pk=patient_id)

    if patient.admitted:
        patient.admitted = False
    else:
        patient.admitted = True

    patient.save()
    labels = ["Name", "Email", "Birthday", "Hospital", "Admission Status"]
    context = {"Patients": Patient.objects.all(), "Labels": labels}

    return render(request, 'core/view_patients.html', context)


class NewHospital(CreateView, UserPassesTestMixin, LoginRequiredMixin):
    """
    View class for Hospital admins to make new hospital instances.
    """
    model = Hospital

    template_name = 'core/new_hospital.html'

    form_class = NewHospitalForm

    success_url = reverse_lazy('landing')

    def test_func(self):
        return is_admin(self.request.user)


class ViewPatientMediInfo(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Viewer for patient Medical Info by nurses or Doctors
    """
    model = Patient

    template_name = 'core/view_medi_info.html'

    def get_context_data(self, **kwargs):
        context = super(ViewPatientMediInfo, self).get_context_data(**kwargs)
        p_id = self.kwargs['patient_id']
        context['Patient'] = Patient.objects.get(pk=p_id)
        context['is_doctor'] = is_doctor(self.request.user)
        return context

    def get_object(self, queryset=None):
        p_id = self.kwargs['patient_id']
        patient = Patient.objects.get(pk=p_id)
        log = Log.objects.create_Log(self.request.user, self.request.user.username, timezone.now(), "Patient(\"" +
                                     patient.user.get_full_name() + "\", id " + p_id + ") Medical Info viewed")
        log.save()
        return patient

    def test_func(self):
        return is_doctor_or_nurse(self.request.user)
