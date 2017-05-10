from django.test import TestCase
from .models import Results, ResultsManager
from core.models import Nurse, Doctor, Admin, Patient, Hospital
from django.contrib.auth.models import User, Group
from django.utils import timezone


class ResultsTestCase(TestCase):
    """
    Test case that handles all testing of Test Results
    """

    def setUp(cls):
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

        cls.patient1 = Patient.create(cls.P_user, "1/1/1960", "M", "A-", "75", "190", "Death", "Type 2 Diabetes",
                                     "Geico", "Hospital1", "emerg@contact.com")

        cls.doctor = Doctor.create(cls.D_user, cls.hospital, "4438483228")

        Results.objects.create(name="Test", notes="This is a test", patient=None, files='results.png', doctor=cls.D_user, date=timezone.now(), released=False)
        Results.objects.create(name="Test2", notes="This is a test", patient=None, files=None, doctor=cls.D_user, date=timezone.now(), released=False)

    def test_result_made(self):
        """
        Tests to make sure result is create
        :return: True if result is created
        """
        res1 = Results.objects.get(name="Test")
        self.assertEqual(res1.notes, 'This is a test')

    def test_no_file(self):
        """
        Raises error if file does not exisit
        :return: true if error occurs
        """
        res2 = Results.objects.get(name="Test2")
        self.assertRaises(TypeError, res2.files, None)
