from django import forms
from .models import Doctor, Appointment

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["name", "email", "specialty", "phone", "availability", "fee", "bio"]

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient_name", "patient_email", "patient_phone", "doctor", "appointment_time"]
        widgets = {
            "appointment_time": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }
