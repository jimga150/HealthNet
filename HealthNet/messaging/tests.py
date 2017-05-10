from django.test import TestCase
from .models import Message, MessageManager
from core.models import Nurse, Doctor, Admin, Patient, Hospital
from django.contrib.auth.models import User, Group
from django.utils import timezone


class MessageTestCase(TestCase):
    """
    Test case that handles all testing of Messaging
    """

    def setUp(cls):
        Group.objects.create(name='Patient')
        Group.objects.create(name='Doctor')
        Group.objects.create(name='Nurse')
        Group.objects.create(name='Admin')
        Hospital.objects.create(name="Hospital1")

        cls.P_user = User.objects.create(username="TestPatient", password="password", email="Patient@Patient.com",
                                         first_name="PTest", last_name="LastName")
        cls.N_user = User.objects.create(username="TestNurse", password="password", email="Nurse@Patient.com",
                                         first_name="NTest", last_name="LastName")
        cls.D_user = User.objects.create(username="TestDoctor", password="password", email="Doctor@Patient.com",
                                         first_name="DTest", last_name="LastName")
        cls.A_user = User.objects.create(username="TestAdmin", password="password", email="Admin@Patient.com",
                                         first_name="ATest", last_name="LastName")


        Message.objects.create(sender=cls.P_user, recipient=cls.D_user, text="Test1", subject="This is a Test",
                               date=timezone.now(), viewed=False)
        Message.objects.create(sender=cls.P_user, recipient=cls.A_user, text="Test2", subject="", date=timezone.now(),
                               viewed=False)

    def test_correct_fields(self):
        """
        Tests to make sure message is created
        :return: True if fields match
        """
        mess1 = Message.objects.get(text="Test1")
        self.assertEqual(mess1.text, 'Test1')
        self.assertEqual(mess1.subject, 'This is a Test')

    def test_no_subject(self):
        """
        Tests empty fields
        :return: True if fields are empty
        """
        mess2 = Message.objects.get(text="Test2")
        self.assertEqual(mess2.text, 'Test2')
        self.assertEqual(mess2.subject, '')
