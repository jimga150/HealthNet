from core.models import Patient, Doctor, Hospital
from django.db import models


class AppointmentManager(models.Manager):
    """
    AppointmentManager represents the manager for the Appointment class, allowing for easier creation
    """

    def create_appointment(self, patient, doctor, appointmentStart, office):
        appointment = self.create(patient=patient, doctor=doctor, office=office,
                                  appointmentStart=appointmentStart)
        return appointment


class Appointment(models.Model):
    """
    Appointment is the model, and it holds the patient and doctor that are involved in the appointment, as well as
    the hospital that the appointment is taking place at, the time of the appointment, and any notes
    """
    patient = models.ForeignKey(Patient, related_name='patient')
    doctor = models.ForeignKey(Doctor, related_name='doctor')
    hospital = models.ForeignKey(Hospital, related_name='hospital')
    appointmentStart = models.DateTimeField("Appointment Start (YYYY-MM-DD HH:MM)", null=True)
    appointmentEnd = models.DateTimeField("Appointment End (YYYY-MM-DD HH:MM)", null=True)
    appointmentNotes = models.CharField(max_length=500)

    # Object manager for appointments, to create the model
    objects = AppointmentManager()
