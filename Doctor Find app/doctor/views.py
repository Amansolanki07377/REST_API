from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from .models import Doctor, Appointment
from .forms import DoctorForm, AppointmentForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils import timezone
import json

def home(request):
    return render(request, "home.html")

def contact(request):
    return render(request, "contact.html")

def doctor_list(request):
    doctors = Doctor.objects.all().order_by("name")
    return render(request, "doctor/doctor_list.html", {"doctors": doctors})

def profile(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, "doctor/profile.html", {"doctor": doctor})

# CRUD HTML pages (non-AJAX)
def doctor_add(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("doctor:doctor_list")
    else:
        form = DoctorForm()
    return render(request, "doctor/doctor_form.html", {"form": form, "title": "Add Doctor"})

def doctor_edit(request, pk):
    d = get_object_or_404(Doctor, pk=pk)
    if request.method == "POST":
        form = DoctorForm(request.POST, instance=d)
        if form.is_valid():
            form.save()
            return redirect("doctor:doctor_list")
    else:
        form = DoctorForm(instance=d)
    return render(request, "doctor/doctor_form.html", {"form": form, "title": "Edit Doctor"})

def doctor_delete(request, pk):
    d = get_object_or_404(Doctor, pk=pk)
    if request.method == "POST":
        d.delete()
        return redirect("doctor:doctor_list")
    return render(request, "doctor/doctor_confirm_delete.html", {"doctor": d})

# ---------- AJAX / API endpoints ------------
from django.views.decorators.http import require_POST

@require_POST
def api_doctor_add(request):
    form = DoctorForm(request.POST)
    if form.is_valid():
        doctor = form.save()
        return JsonResponse({"status": "ok", "id": doctor.id})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)

@require_POST
def api_doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    form = DoctorForm(request.POST, instance=doctor)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)

@require_POST
def api_doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.delete()
    return JsonResponse({"status": "deleted"})

# ---------- Appointment registration with client-side validation ----------
def appointment_register(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # For demo: mark not paid
            appointment.paid = False
            appointment.save()
            # Redirect to payment initiation or show confirmation
            return redirect("doctor:paytm_initiate", appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, "doctor/appointment_register.html", {"form": form})

# ---------- Paytm integration placeholders ----------
def paytm_initiate(request, appointment_id):
    # This is a placeholder page. For real integration:
    # - Create order with Paytm params, compute checksum using merchant key
    # - Send the user to Paytm payment URL with POST form
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    context = {"appointment": appointment, "paytm_mid": "YOUR_MID", "txn_amount": str(appointment.doctor.fee)}
    return render(request, "doctor/paytm_initiate.html", context)

@csrf_exempt
def paytm_callback(request):
    # Placeholder to receive callback from Paytm after payment
    # Verify checksum and update appointment.paid accordingly
    # For demo, accept POST and mark appointment paid if appointment_id present
    if request.method == "POST":
        appt_id = request.POST.get("ORDER_ID") or request.POST.get("appointment_id")
        if appt_id:
            try:
                appt = Appointment.objects.get(pk=int(appt_id))
                appt.paid = True
                appt.save()
                return render(request, "doctor/paytm_success.html", {"appointment": appt})
            except Appointment.DoesNotExist:
                return HttpResponseBadRequest("Unknown appointment")
    return HttpResponse("Callback received (demo)")

# ---------- Simple auth views (demo) ----------
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import HttpResponseRedirect

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("doctor:home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("doctor:home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("doctor:home")

