from django.db import models
from django.utils.translation import gettext_lazy as _


class MetricChoices(models.TextChoices):
        BLOOD_SUGAR = 'blood_sugar', _('Цукор в крові')
        BLOOD_PRESSURE = 'blood_pressure', _('Тиск')
        HEART_RATE = 'heart_rate', _('Пульс')
        TEMPERATURE = 'temperature', _('Температура')
        CHOLESTEROL = 'cholesterol', _('Холестерин')



class GenderChoices(models.TextChoices):
        MALE = 'male', _('Чоловік')
        FEMALE = 'female', _('Жінка')
        OTHER = 'other', _('Інше')



class RoleChoices(models.TextChoices):
        PATIENT = 'patient', _('Пацієнт')
        DOCTOR = 'doctor', _('Лікар')
