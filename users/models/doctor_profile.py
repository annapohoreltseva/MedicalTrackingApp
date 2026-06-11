from django.contrib.auth import get_user_model
from django.db import models


class DoctorProfile(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
