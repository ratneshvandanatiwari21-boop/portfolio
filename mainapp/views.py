from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .models import ContactMessage


def index(request):
    if request.method == "POST":
        form_values = {
            "name": request.POST.get("name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "subject": request.POST.get("subject", "").strip(),
            "message": request.POST.get("message", "").strip(),
        }

        if not all(form_values.values()):
            messages.error(request, "Please fill all fields before sending your message.")
            return render(request, "index.html", {"form_values": form_values})

        try:
            validate_email(form_values["email"])
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return render(request, "index.html", {"form_values": form_values})

        ContactMessage.objects.create(**form_values)
        messages.success(request, "Message sent successfully. I will contact you soon.")
        return redirect("/#contact")

    return render(request, "index.html")
