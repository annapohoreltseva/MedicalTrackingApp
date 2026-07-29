from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import DoctorProfile, HealthMetric, PatientProfile
from .models.choices import GenderChoices, RoleChoices

User = get_user_model()


class HealthMetricForm(forms.ModelForm):
    class Meta:
        model = HealthMetric
        fields = [
            "patient",
            "added_by",
            "metric_type",
            "value",
            "unit",
            "measured_at",
            "notes",
        ]
        widgets = {
            "measured_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "Optional notes or observations...",
                }
            ),
            "patient": forms.Select(attrs={"class": "form-control"}),
            "added_by": forms.Select(attrs={"class": "form-control"}),
            "metric_type": forms.Select(attrs={"class": "form-control"}),
            "value": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "any",
                    "placeholder": "e.g. 120 or 5.5",
                }
            ),
            "unit": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. mmHg, mg/dL, bpm, °C",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default datetime for new metrics to current local time if not provided
        if not self.initial.get("measured_at") and not self.instance.pk:
            self.initial["measured_at"] = timezone.now().strftime("%Y-%m-%dT%H:%M")

        # Configure patient and added_by choices
        patients_qs = User.objects.filter(role=RoleChoices.PATIENT)
        if patients_qs.exists():
            self.fields["patient"].queryset = patients_qs
        else:
            self.fields["patient"].queryset = User.objects.all()

        self.fields["added_by"].queryset = User.objects.all()
        self.fields["added_by"].required = False
        self.fields["patient"].empty_label = "Select Patient..."
        self.fields[
            "added_by"
        ].empty_label = "Select Practitioner / Added By (Optional)..."


class PatientCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g. John"}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g. Doe"}
        ),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "john.doe@example.com"}
        ),
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    gender = forms.ChoiceField(
        choices=GenderChoices.choices,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. jdoe (Optional, auto-generated if empty)",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = RoleChoices.PATIENT
        first = self.cleaned_data.get("first_name", "").strip()
        last = self.cleaned_data.get("last_name", "").strip()
        user.first_name = first
        user.last_name = last

        if not user.username:
            base_name = f"{first.lower()}{last.lower()}".replace(" ", "") or "patient"
            count = User.objects.filter(username__startswith=base_name).count()
            user.username = f"{base_name}{count + 1}" if count > 0 else base_name

        if commit:
            user.save()
            PatientProfile.objects.create(
                user=user,
                first_name=first,
                last_name=last,
                birth_date=self.cleaned_data.get("birth_date"),
                gender=self.cleaned_data.get("gender") or GenderChoices.OTHER,
            )
        return user


class DoctorCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g. Sarah"}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g. Smith"}
        ),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "dr.smith@example.com"}
        ),
    )
    specialty = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. Cardiology, Pediatrics",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. drsmith (Optional, auto-generated if empty)",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = RoleChoices.DOCTOR
        first = self.cleaned_data.get("first_name", "").strip()
        last = self.cleaned_data.get("last_name", "").strip()
        specialty = self.cleaned_data.get("specialty", "").strip()
        user.first_name = first
        user.last_name = last

        if not user.username:
            base_name = f"dr_{first.lower()}{last.lower()}".replace(" ", "") or "doctor"
            count = User.objects.filter(username__startswith=base_name).count()
            user.username = f"{base_name}{count + 1}" if count > 0 else base_name

        if commit:
            user.save()
            DoctorProfile.objects.create(
                user=user, first_name=first, last_name=last, specialty=specialty
            )
        return user
