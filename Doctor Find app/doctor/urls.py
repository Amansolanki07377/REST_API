from django.urls import path
from . import views

app_name = "doctor"

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path("contact/", views.contact, name="contact"),
    # CRUD pages
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("doctors/add/", views.doctor_add, name="doctor_add"),
    path("doctors/<int:pk>/edit/", views.doctor_edit, name="doctor_edit"),
    path("doctors/<int:pk>/delete/", views.doctor_delete, name="doctor_delete"),
    # AJAX endpoints
    path("api/doctors/add/", views.api_doctor_add, name="api_doctor_add"),
    path("api/doctors/<int:pk>/edit/", views.api_doctor_edit, name="api_doctor_edit"),
    path("api/doctors/<int:pk>/delete/", views.api_doctor_delete, name="api_doctor_delete"),
    # Appointment and payment
    path("appointments/register/", views.appointment_register, name="appointment_register"),
    path("pay/<int:appointment_id>/", views.paytm_initiate, name="paytm_initiate"),
    path("pay/callback/", views.paytm_callback, name="paytm_callback"),
    # auth (simple wrappers)
    path("accounts/signup/", views.signup_view, name="signup"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
]
