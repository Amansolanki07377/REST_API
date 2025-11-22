function validateEmail(email) {
  // simple regex
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

function validatePhone(phone) {
  const onlyDigits = phone.replace(/\D/g,'');
  return onlyDigits.length >= 10 && onlyDigits.length <= 15;
}

function showError(el, msg) {
  // simple alert or add inline message, here we use alert for demo
  alert(msg);
  el.focus();
}

function validateAppointmentForm(form) {
  const email = form.querySelector('[name="patient_email"]');
  const phone = form.querySelector('[name="patient_phone"]');
  const name = form.querySelector('[name="patient_name"]');

  if(!name || name.value.trim() === "") {
    showError(name, "Please enter your name");
    return false;
  }
  if(!email || !validateEmail(email.value)) {
    showError(email, "Enter a valid email");
    return false;
  }
  if(!phone || !validatePhone(phone.value)) {
    showError(phone, "Enter a valid phone number (10+ digits)");
    return false;
  }
  return true;
}
