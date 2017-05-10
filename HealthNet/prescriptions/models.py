from django.db import models
from django.utils import timezone

from core.models import Patient, Doctor


class Prescription(models.Model):
    """
    Defines a Prescription
    """
    patient = models.ForeignKey(Patient, verbose_name='Patient')
    doctor = models.ForeignKey(Doctor, verbose_name="Doctor")
    date_prescribed = models.DateTimeField()

    drug = models.CharField(max_length=500)

    dosage = models.DecimalField(max_digits=6, decimal_places=3)
    DOSE_CHOICES = (
        ("mg", "milligrams"),
        ("ug", "micrograms"),
        ("pg", "picograms"),
        ("g", "grams")
    )
    Dose_units = models.CharField(max_length=10, choices=DOSE_CHOICES, default="mg")

    rate = models.PositiveSmallIntegerField()
    TIME_CHOICES = (
        ("/D", "per Day"),
        ("/h", "per Hour"),
        ("/W", "per Week"),
        ("/M", "per Month")
    )
    Time_units = models.CharField(max_length=9, choices=TIME_CHOICES, default="/D")

    def __str__(self):
        return str(self.patient) + ": " + str(self.rate) + " dose(s) of " + str(self.dosage) + " " + \
               str(dict(self.DOSE_CHOICES)[self.Dose_units]) + " of " + str(self.drug) + " " + \
               str(dict(self.TIME_CHOICES)[self.Time_units])

    @classmethod
    def fromString(cls, Prescription_string, patient_id, doctor_user):
        """
        Constructs an instance of a Prescription by reading one of its own __str__ exports.
        :param Prescription_string: String representation of the Prescription
        :param patient_id: ID of the patient being prescribed to
        :param doctor_user: User of Doctor who is signing off on this import.
        :return: Saved Prescription
        """
        words = Prescription_string.split(" ")
        if len(words) != 11:
            print("Cannot make prescription from String [" + Prescription_string + "]")
            return None
        patient = Patient.objects.get(pk=patient_id)
        rate = int(words[2])
        dosage = float(words[5])

        Dose_units = "mg"
        Dose_units_verbose = words[6]
        for d in Prescription.DOSE_CHOICES:
            if d[1] == Dose_units_verbose:
                Dose_units = d[0]

        drug = words[8]

        Time_units = "/D"
        Time_units_verbose = words[9] + " " + words[10]
        for t in Prescription.TIME_CHOICES:
            if t[1] == Time_units_verbose:
                Time_units = t[0]

        tosave =  cls(patient=patient, doctor=Doctor.objects.get(user=doctor_user), date_prescribed=timezone.now(),
                   drug=drug, dosage=dosage, Dose_units=Dose_units, rate=rate, Time_units=Time_units)
        tosave.save()
        return tosave
