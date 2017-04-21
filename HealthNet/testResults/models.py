from django.db import models
from django.contrib.auth.models import User
from core.models import Patient

class ResultsManager(models.Manager):

    def create_test(self, name, notes, files, patient, doctor, date):
        result = self.create(name=name, notes=notes, files=files, patient=patient, doctor=doctor, date=date)
        return result

class Results(models.Model):

    name = models.CharField(max_length=100, blank=True)
    notes = models.CharField(max_length=500, blank=True)
    patient = models.ForeignKey(Patient,  related_name='Test_Patient', null=True)
    files = models.FileField(upload_to='testResults', null=True)
    doctor = models.ForeignKey(User, related_name='Test_Doctor', null=True)
    date = models.DateField()
    released = models.BooleanField(default=False)

    objects = ResultsManager()

    def __str__(self):
        return self.name