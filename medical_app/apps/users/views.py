from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import DoctorCreateForm, HealthMetricForm, PatientCreateForm
from .models import HealthMetric
from .models.choices import RoleChoices

User = get_user_model()


# Create your views here.


class MedicalHomeView(TemplateView):
    template_name = "medical_app/home.html"


class MedicalAboutView(TemplateView):
    template_name = "medical_app/about.html"


class HealthMetricListView(ListView):
    model = HealthMetric
    template_name = "health_metric/health_metric.html"
    context_object_name = "health_metrics"


class HealthMetricDetailView(DetailView):
    model = HealthMetric
    template_name = "health_metric/health_metric_detail.html"


class HealthMetricCreateView(CreateView):
    model = HealthMetric
    form_class = HealthMetricForm
    template_name = "health_metric/health_metric_detail_form.html"
    success_url = reverse_lazy("health_metric")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patients_count"] = (
            User.objects.filter(role=RoleChoices.PATIENT).count()
            or User.objects.count()
        )
        return context

    def form_valid(self, form):
        if not form.instance.added_by_id and self.request.user.is_authenticated:
            form.instance.added_by = self.request.user
        if not form.instance.patient_id and self.request.user.is_authenticated:
            form.instance.patient = self.request.user
        return super().form_valid(form)


class HealthMetricUpdateView(UpdateView):
    model = HealthMetric
    form_class = HealthMetricForm
    template_name = "health_metric/health_metric_detail_form.html"
    success_url = reverse_lazy("health_metric")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patients_count"] = (
            User.objects.filter(role=RoleChoices.PATIENT).count()
            or User.objects.count()
        )
        return context


class HealthMetricDeleteView(DeleteView):
    model = HealthMetric
    template_name = "health_metric/health_metric_delete.html"
    success_url = reverse_lazy("health_metric")


class PatientListView(ListView):
    model = User
    template_name = "patient/patient_list.html"
    context_object_name = "patients"

    def get_queryset(self):
        return User.objects.filter(role=RoleChoices.PATIENT)


class PatientCreateView(CreateView):
    model = User
    form_class = PatientCreateForm
    template_name = "patient/patient_form.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("patient_list")


class DoctorListView(ListView):
    model = User
    template_name = "doctor/doctor_list.html"
    context_object_name = "doctors"

    def get_queryset(self):
        return User.objects.filter(role=RoleChoices.DOCTOR).select_related(
            "doctorprofile"
        )


class DoctorCreateView(CreateView):
    model = User
    form_class = DoctorCreateForm
    template_name = "doctor/doctor_form.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("doctor_list")
