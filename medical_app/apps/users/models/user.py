from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import *


class User(AbstractUser):
    role = models.CharField(max_length=10, choices=RoleChoices)

    def __str__(self):
        full_name = self.get_full_name()
        if (
            not full_name
            and hasattr(self, "patientprofile")
            and (self.patientprofile.first_name or self.patientprofile.last_name)
        ):
            full_name = f"{self.patientprofile.first_name} {self.patientprofile.last_name}".strip()
        if (
            not full_name
            and hasattr(self, "doctorprofile")
            and (self.doctorprofile.first_name or self.doctorprofile.last_name)
        ):
            full_name = f"{self.doctorprofile.first_name} {self.doctorprofile.last_name}".strip()

        role_display = self.get_role_display() if self.role else ""
        if full_name:
            return f"{full_name} ({self.username})" + (
                f" - {role_display}" if role_display else ""
            )
        return f"{self.username}" + (f" ({role_display})" if role_display else "")

    class Meta:
        app_label = "users"
