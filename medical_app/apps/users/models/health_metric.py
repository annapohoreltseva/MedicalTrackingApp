from django.conf import settings
from django.db import models
from django.urls import reverse

from .choices import MetricChoices


class HealthMetric(models.Model):
    patient = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_metrics",
    )
    added_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="added_metrics",
    )
    metric_type = models.CharField(max_length=50, choices=MetricChoices)
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    measured_at = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("health_metric_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.get_metric_type_display() if hasattr(self, 'get_metric_type_display') else self.metric_type}: {self.value} {self.unit}"

    class Meta:
        app_label = "users"
