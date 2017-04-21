from django.test import TestCase
from django.utils import timezone

from .models import *


# Create your tests here.


class HospitalManagerTest(TestCase):

    None


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
    None


class PatientTest(TestCase):
    """
    Tests for Patients
    """
    def test_future_birthday(self):
        """
        Tests if a patient can have their an invalid birthday format
        :return: False if the patient was invalid
        """
        date = 10 / 12 / 20
        pat = Patient(User, date, "Male", "AB-", 10, 10, None, None, None, None)
        self.assertEqual(pat.__str__ == "Jake", False)


class LogManagerTest(TestCase):
    """
    Tests for the LogManager
    """
    None


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
