from django.test import TestCase
from django.utils import timezone

from .models import *
from .views import *


# Create your tests here.


class HospitalManagerTest(TestCase):
    pass


class HospitalTest(TestCase):
    """
    Tests for Hospitals
    """

    def test_create_hospital(self):
        """
        Ensures that a hospital can be created
        :return: True if the hospital was created
        """
        hos = Hospital(name="Test")
        self.assertEqual(hos.__str__ == "Test", False)


class NurseTest(TestCase):
    """
    Tests for Nurses
    """

    def test_nurse_prof(self):
        """
        Ensures a nurse can be created
        :return: True if the nurse was created
        """
        nurse = Nurse(User, "RIT", "634-1242")
        self.assertEqual(nurse.__str__ == "Sally", False)


class DoctorTest(TestCase):
    """
    Tests for Doctors
    """
    def test_doc_prof(self):
        """
        Ensures a doctor can be created
        :return: True if the doctor was created
        """
        user = User.objects.create_user(username='Who', first_name="Doctor", last_name="Who", email='jacob@…', password='top_secret')
        user.save()
        doctor = Doctor(user, "634-1242")
        self.assertEqual(user.username is "Who", True)
        self.assertEqual(doctor.__str__ == "Billy Bob", False)


class PatientTest(TestCase):
    """
    Tests for Patients
    """

    @classmethod
    def setUp(cls):
        Group.objects.create(name='Patient')
        cls.P_user = User.objects.create(username="TestPatient", password="password", email="Patient@Patient.com",
                                         first_name="PTest", last_name="LastName")
        cls.D_user = User.objects.create(username="TestDoctor", password="password", email="Doctor@Patient.com",
                                         first_name="DTest", last_name="LastName")
        Hospital.objects.create(name="Hospital1")

    def test_future_birthday(self):
        """
        Tests if a patient can have their an invalid birthday format
        :return: False if the patient was invalid
        """
        date = 10 / 12 / 20
        pat = Patient(User, date, "Male", "AB-", 10, 10, None, None, None, None)
        self.assertEqual(pat.__str__ == "Jake", False)

    def test_emergency_contact(self):
        """
                Tests if the emergency contact user is filled if a user with the given email exists
                :return: False if the emergency contact auto fill does not work
                """
        pat1 = Patient.create(self.P_user, "1998-02-26", "M", "A+", "Heavy", 123, "Peanuts", "Died once", "Blue Cross",
                              "Hospital1", "Doctor@Patient.com")

        pat2 = Patient.create(self.P_user, "1998-02-26", "M", "A+", "Heavy", 123, "Peanuts", "Died once", "Blue Cross",
                              "Hospital1", "Nonsense@Nosuch.com")
        # If the emergency contact is filled with a valid email
        self.assertEqual(pat1.emergency_contact_user is None, False)

        # If the emergency contact is filled with an invalid email
        self.assertEqual(pat2.emergency_contact_user is None, True)

class LogManagerTest(TestCase):
    """
    Tests for the LogManager
    """
    pass


class LogTest(TestCase):
    """
    Tests for the logs
    """

    def test_create_log(self):
        """
        Tests if a log can be created
        :return: True if the log was successfully created
        """
        log = Log(User, "Test", timezone.now(), "Test")
        self.assertEqual(log.__str__ == "Test", False)


class UtilityFunctions(TestCase):
    """
    Tests all utility functions
    """

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='Patient')
        Group.objects.create(name='Doctor')
        Group.objects.create(name='Nurse')
        Group.objects.create(name='Admin')
        cls.hospital = Hospital.objects.create(name="Hospital1")

        cls.P_user = User.objects.create(username="TestPatient", password="password", email="Patient@Patient.com",
                                         first_name="PTest", last_name="LastName")
        cls.N_user = User.objects.create(username="TestNurse", password="password", email="Nurse@Patient.com",
                                         first_name="NTest", last_name="LastName")
        cls.D_user = User.objects.create(username="TestDoctor", password="password", email="Doctor@Patient.com",
                                         first_name="DTest", last_name="LastName")
        cls.A_user = User.objects.create(username="TestAdmin", password="password", email="Admin@Patient.com",
                                         first_name="ATest", last_name="LastName")

        cls.patient = Patient.create(cls.P_user, "1/1/1980", "M", "B-", "65", "180", "Pollen", "Type 2 Diabetes",
                                     "Geico", "Hospital1", "emerg@contact.com")
        # print(cls.P_user.groups)

        cls.nurse = Nurse.create(cls.N_user, "Hospital1", "2408937770")
        # print(cls.N_user.groups)

        cls.doctor = Doctor.create(cls.D_user, cls.hospital, "4438483228")
        # print(cls.D_user.groups)

        cls.admin = Admin.create(cls.A_user)
        # print(cls.A_user.groups)

    def test_user_checks(self):
        self.assertTrue(is_patient(self.P_user))
        self.assertFalse(is_admin(self.P_user))
        self.assertFalse(is_doctor(self.P_user))
        self.assertFalse(is_nurse(self.P_user))

        self.assertFalse(is_patient(self.D_user))
        self.assertFalse(is_admin(self.D_user))
        self.assertTrue(is_doctor(self.D_user))
        self.assertFalse(is_nurse(self.D_user))

        self.assertFalse(is_patient(self.N_user))
        self.assertFalse(is_admin(self.N_user))
        self.assertFalse(is_doctor(self.N_user))
        self.assertTrue(is_nurse(self.N_user))

        self.assertFalse(is_patient(self.A_user))
        self.assertTrue(is_admin(self.A_user))
        self.assertFalse(is_doctor(self.A_user))
        self.assertFalse(is_nurse(self.A_user))

    def test_utilities(self):
        self.maxDiff = None
        self.assertEqual(QueryListtoString(User.objects.all()), 'TestPatient\nTestNurse\nTestDoctor\nTestAdmin\n')
        self.assertTrue(MediInfoExport(self.patient, self.P_user, True).__contains__('Hello PTest,'))
        self.assertTrue(MediInfoExport(self.patient, self.P_user, False).__contains__('emerg@contact.com'))
        self.assertEqual(listtostring(list(User.objects.all())), 'TestPatient TestNurse TestDoctor TestAdmin')
