from django.contrib.auth.models import User, Group
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class HospitalManager(models.Manager):
    """
    HospitalManager: manager for the hospital class.
    hospital - Hospital object
    """
    def create_hospital(self, name):
        hospital = self.create(name=name)
        return hospital


class Hospital(models.Model):
    """
    Hospital: location that all user types have. Can be edited by Doctors/Admins.
    name - string for hospital's name
    """
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Nurse(models.Model):
    """
    Nurse: employee user class that can edit specific information and admit Patients.
    user - the User object that is extended
    hospital - the hospital object that the nurse is located at
    phoneNum - string with nurse's phone contact ('xxx-xxx-xxxx')
    """
    user = models.OneToOneField(User)
    hospital = models.ForeignKey(Hospital)
    phoneNum = models.CharField(max_length=11)

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create(cls, user, hospital_string, phoneNum_string):
        user.groups.add(Group.objects.get(name='Nurse'))
        return cls(user=user, hospital=Hospital.objects.get(name=hospital_string), phoneNum=phoneNum_string)


class Doctor(models.Model):
    """
    Doctor: employee user class that can edit Patient info, set up Appointments, release test information,
            and admit Patients.
    user - the User object that is extended
    phoneNum - string with doctor's phone contact ('xxx-xxx-xxxx')
    """
    user = models.OneToOneField(User)
    hospital = models.ForeignKey(Hospital)
    phoneNum = models.CharField(max_length=11)

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create(cls, user, hospital_string, phoneNum_string):
        user.groups.add(Group.objects.get(name='Doctor'))
        return cls(user=user, hospital=Hospital.objects.get(name=hospital_string), phoneNum=phoneNum_string)


class Admin(models.Model):
    """
    Admin: employee user class that can access logs
    user - the User object that is extended

    """
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create(cls, user):
        user.groups.add(Group.objects.get(name='Admin'))
        return cls(user=user)


class Patient(models.Model):
    """
    Patient: One to one relationship with the User model in order to manage all patients as individual users. Contains
    info pertinent to Doctors and Nurses, such as Blood type and height/weight.
    
    user - links to associated User
    
    birthday - date used to determine age
    
    sex - biological sex, since doctors are concerned with anatomy and hormone balance. 3rd option is provided in
    ambiguous cases.
    
    blood type - simple, on of the 8 possible blood types or unknown
    
    height - currently an integer as one's height in inches
    
    weight - one's weight in pounds
    
    allergies - for now this is a simple text field, but soon this will be a comma separated list of one's allergies
    that will be made browsable (R2) by the Doctor
    
    insurance info - simple character field meant to store one's insurance ID.
    
    preferred hospital - used when a patient has a choice of hospital
    
    hospital - Hospital that the Patient is currently in
    
    emergency contact - self explanatory, can also be linked to another user in the hospital
    
    emergency contact user - links to user (if one exists) in the system that matches the email in the field above
    
    admitted - true if currently admitted, false otherwise
    """
    user = models.OneToOneField(User)
    birthday = models.DateField(default="1800-01-01")
    SEX_CHOICE = (
        ("M", "Male"),
        ("F", "Female"),
        ("N", "Neither"),
    )
    sex = models.CharField(max_length=5, choices=SEX_CHOICE, default="M")
    BLOOD_TYPE = (
        ("A+", "A+"),
        ("B+", "B"),
        ("O+", "O+"),
        ("AB+", "AB+"),
        ("A-", "A-"),
        ("B-", "B-"),
        ("O-", "O-"),
        ("AB-", "AB-"),
        ("UN", "Unknown"),
    )
    blood_type = models.CharField(max_length=10, choices=BLOOD_TYPE, default="UN")
    height = models.CharField(max_length=7, null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    allergies = models.TextField(max_length=1000, default="")
    medical_history = models.TextField(max_length=1000, default="")

    insurance_info = models.CharField(max_length=50)
    preferred_hospital = models.ForeignKey(Hospital, null=True, related_name="preferred_hospital")
    hospital = models.ForeignKey(Hospital, null=False, related_name="current_hospital")
    emergency_contact = models.EmailField()
    emergency_contact_user = models.ForeignKey(User, null=True, related_name='emergency_user')

    admitted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create(cls, user, birthday_string, sex_verbose, b_type, height, weight, allergies, med_hist, insurance,
               p_hos_string, emerg_con_email):
        try:
            emerg_con_user = User.objects.get(email=emerg_con_email)
        except ObjectDoesNotExist:
            emerg_con_user = None

        user.groups.add(Group.objects.get(name='Patient'))

        return cls(user=user, birthday=birthday_string, sex=sex_verbose,
                   blood_type=b_type, height=height, weight=weight, allergies=allergies, medical_history=med_hist,
                   insurance_info=insurance, preferred_hospital=Hospital.objects.get(name=p_hos_string),
                   hospital=Hospital.objects.get(name=p_hos_string), emergency_contact=emerg_con_email,
                   emergency_contact_user=emerg_con_user, admitted=True)


class LogManager(models.Manager):
    """
    LogManager: Manages Logs
    log - Log created to be stored
    """
    def create_Log(self, user, username, time, log_type):
        log = self.create(user=user, username=username, time=time, type=log_type)
        return log


class Log(models.Model):
    """
    Log: contains a single log entry.
    user - the USer who generated this entry
    username - self explanatory
    time - the time this action was logged
    type - what action was performed
    """
    user = models.ForeignKey(User, verbose_name='User')
    username = models.CharField(default='', max_length=100, verbose_name='Username')

    time = models.DateTimeField(verbose_name='Date Logged')
    type = models.CharField(max_length=100, verbose_name='Type')

    objects = LogManager()

    def __str__(self):
        return self.type
