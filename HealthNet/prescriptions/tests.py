from django.test import TestCase
from django.contrib.auth.models import User, Group
from core.models import Patient, Doctor, Hospital
from .models import Prescription


class CreatePrescriptionTests(TestCase):
    """
    Tests for creating prescriptions
    """

    @classmethod
    def setUp(cls):
        Group.objects.create(name='Patient')
        Group.objects.create(name='Doctor')
        Group.objects.create(name='Nurse')
        Group.objects.create(name='Admin')
        cls.hospital = Hospital.objects.create(name="Hospital1")
        cls.P_user = User.objects.create(username="TestPatient", password="password", email="Patient@Patient.com",
                                         first_name="PTest", last_name="LastName")
        cls.D_user = User.objects.create(username="TestDoctor", password="password", email="Doctor@Patient.com",
                                         first_name="DTest", last_name="LastName")

        cls.patient = Patient.objects.create(user=cls.P_user, birthday="1980-1-1", sex="M", blood_type="B-",
                                             height="65", weight="180", allergies="Pollen",
                                             medical_history="Type 2 Diabetes", insurance_info="Geico",
                                             hospital=cls.hospital, emergency_contact="emerg@contact.com"
                                             )
        # print("Patient ID: " + str(cls.patient.id))
        cls.doctor = Doctor.objects.create(user=cls.D_user, hospital=cls.hospital, phoneNum="4438483228")

    def test_blank_prescription_str(self):
        # print("Patient ID: " + str(self.patient.id))
        prescription_test = Prescription.fromString('', self.patient.id, self.doctor.user)

        self.assertEqual(prescription_test, None)

    def test_prescription(self):
        prescription = Prescription.fromString('PTest LastName: 10 doses of 2 mg of Drug per day', self.patient.id,
                                               self.doctor.user)

        self.assertEqual(prescription.__str__(), 'PTest LastName: 10 dose(s) of 2.0 milligrams of Drug per Day')
