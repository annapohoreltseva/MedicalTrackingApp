from django.contrib.auth import get_user_model
from django.db import models

from users.models.choices import GenderChoices


class PatientProfile(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices)
    height_cm = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
