from core.models import Patient, Doctor, Admin, Hospital, Log
from django.db import models

# Create your models here.


class Transfer(models.Model):
    """
    Transfer: represents a single hospital change for a Patient.
    newHospital - Hospital to move Patient to. (update Patient.hospital)
    patient - Patient to be modified.
    """
    New_Hospital = models.ForeignKey(Hospital)
    patient = models.ForeignKey(Patient)

    def __str__(self):
        return self.patient.__str__() + " was transferred to " + self.New_Hospital.__str__()



