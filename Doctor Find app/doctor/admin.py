

# Register your models here.
from django.contrib import admin
from .models import Doctor, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialty", "phone", "availability", "fee")
    list_filter = ("specialty",)
    search_fields = ("name", "specialty", "email", "phone")
    ordering = ("name",)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient_name", "doctor", "appointment_time", "paid")
    list_filter = ("paid", "doctor")
    search_fields = ("patient_name", "patient_email", "patient_phone")
