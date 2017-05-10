from django.core.urlresolvers import reverse
from django.test import TestCase
from core.models import *


class TheOnlyTestThisNeeds(TestCase):
    """
    The only test that this needs
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

        cls.patient = Patient.objects.create(user=cls.P_user, birthday="1980-1-1", sex="M", blood_type="B-",
                                             height="65", weight="180", allergies="Pollen",
                                             medical_history="Type 2 Diabetes", insurance_info="Geico",
                                             hospital=cls.hospital, emergency_contact="emerg@contact.com"
                                             )
        # print(cls.P_user.groups)

        cls.nurse = Nurse.objects.create(user=cls.N_user, hospital=cls.hospital, phoneNum="2408937770")
        # print(cls.N_user.groups)

        cls.doctor = Doctor.objects.create(user=cls.D_user, hospital=cls.hospital, phoneNum="4438483228")
        # print(cls.D_user.groups)

        cls.admin = Admin.objects.create(user=cls.A_user)
        # print(cls.A_user.groups)

    def test_denying_nologinuser(self):
        response = self.client.get(reverse('statistics'), follow=True)
        self.assertRedirects(response, '/login/?next=/stats/')
        response = self.client.post(reverse('statistics'), follow=True)
        self.assertRedirects(response, '/login/?next=/stats/')

    def test_valid_call(self):
        self.client.login(username='TestAdmin', password='password')
        response = self.client.get(reverse('statistics'))
        self.assertTrue(response.status_code < 400)
