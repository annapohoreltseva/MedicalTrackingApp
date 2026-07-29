from django.urls import path

from .views import (
    DoctorCreateView,
    DoctorListView,
    HealthMetricCreateView,
    HealthMetricDeleteView,
    HealthMetricDetailView,
    HealthMetricListView,
    HealthMetricUpdateView,
    MedicalAboutView,
    MedicalHomeView,
    PatientCreateView,
    PatientListView,
)

urlpatterns = [
    path("", MedicalHomeView.as_view(), name="home"),
    path("about/", MedicalAboutView.as_view(), name="about"),
    path("health_metric", HealthMetricListView.as_view(), name="health_metric"),
    path(
        "health_metric/<int:pk>/",
        HealthMetricDetailView.as_view(),
        name="health_metric_detail",
    ),
    path(
        "health_metric/create_new_metric",
        HealthMetricCreateView.as_view(),
        name="health_metric_create",
    ),
    path(
        "health_metric/<int:pk>/edit",
        HealthMetricUpdateView.as_view(),
        name="health_metric_update",
    ),
    path(
        "health_metric/<int:pk>/delete",
        HealthMetricDeleteView.as_view(),
        name="health_metric_delete",
    ),
    path("patients/", PatientListView.as_view(), name="patient_list"),
    path("patients/create/", PatientCreateView.as_view(), name="patient_create"),
    path("doctors/", DoctorListView.as_view(), name="doctor_list"),
    path("doctors/create/", DoctorCreateView.as_view(), name="doctor_create"),
]
