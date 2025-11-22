

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    specialty = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    availability = models.CharField(max_length=200, blank=True)  # e.g., "Mon-Fri 9am-5pm"
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    bio = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.specialty})"

class Appointment(models.Model):
    patient_name = models.CharField(max_length=200)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=20)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    appointment_time = models.DateTimeField()
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
