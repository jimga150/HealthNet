from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Patient, Doctor
from .models import Prescription


# Create your tests here.


class CreatePrescriptionTests(TestCase):
    date = 12 / 3 / 94
    patient_test = Patient(User, date, "M", "UN", 1, 1, None, None, None, None)
    patient_test.user.first_name("Test")
    patient_test.user.last_name("Test")
    doctor_test = Doctor(User, "1234567890")

    def test_blank_prescription_str(self):
        prescription_test = Prescription.fromString('', 1, doctor_test.user )

        self.assertEqual(prescription_test, None)

    def test_prescription(self):
        prescription = Prescription.fromString('10 doses of 2 mg of Drug per day', 1, doctor_test)

        self.assertEqual(prescription.__str__(),'Test Test: 10 dose(s) of 2 mg of Drug per day', True)


