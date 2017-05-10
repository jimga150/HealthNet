from django.contrib.auth.models import User
from django.test import TestCase

from .models import *
from core.models import Patient, Doctor, Hospital



class AppointmentTests(TestCase):
    """
    Tests for appointments
    """

    def test_create_appointment(self):
        """
        Checks if appointment can be created
        :return: True if the appointment is created
        """

        date = 10 / 12 / 20
        pat = Patient(User, date, "Male", "AB-", 10, 10, None, None, None, None)

        doc = Doctor(User, "634-1242")

        hosp = Hospital(name = 'Hospital 1')

        app = Appointment(patient=pat, doctor=doc, hospital=hosp, appointmentStart='1800-01-01 08:00:00',
                          appointmentNotes='Note!')

        print(app.hospital.name)

        self.assertEqual(app.hospital.name != 'Hospital 2', True)
