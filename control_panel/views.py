from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.forms import modelform_factory
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .panel_registry import PANEL_REGISTRY, GROUP_ORDER

import os
from django.http import Http404, FileResponse
from django.urls import reverse
from django.utils.text import slugify
from main.models import VolunteerApplication

import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST


logger = logging.getLogger(__name__)

def staff_check(user):
    return user.is_active and user.is_staff


class PanelLoginView(auth_views.LoginView):
    template_name = "control_panel/login.html"
    redirect_authenticated_user = True


def _get_entry(slug):
    entry = PANEL_REGISTRY.get(slug)
    if entry is None:
        raise Http404(f"Unknown admin section: {slug}")
    return entry


@login_required(login_url="control_panel:panel_login")
@user_passes_test(staff_check, login_url="control_panel:panel_login")
def dashboard(request):
    groups = {g: [] for g in GROUP_ORDER}
    for slug, entry in PANEL_REGISTRY.items():
        groups.setdefault(entry["group"], []).append({
            "slug": slug,
            "label": entry["label"],
            "count": entry["model"].objects.count(),
        })
    return render(request, "control_panel/dashboard.html", {"groups": groups, "group_order": GROUP_ORDER})


@login_required(login_url="control_panel:panel_login")
@user_passes_test(staff_check, login_url="control_panel:panel_login")
def generic_list(request, slug):
    entry = _get_entry(slug)
    model = entry["model"]

    # A singleton table (Organization) has exactly one row — skip the list
    # and go straight to editing it (or creating it, the first time).
    if entry.get("singleton"):
        obj = model.objects.first()
        if obj:
            return redirect("control_panel:panel_edit", slug=slug, pk=obj.pk)
        return redirect("control_panel:panel_add", slug=slug)

    paginator = Paginator(model.objects.all(), 25)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "control_panel/list.html", {
        "entry": entry, "slug": slug, "page_obj": page,
        "list_fields": entry["list_fields"],
    })


@login_required(login_url="control_panel:panel_login")
@user_passes_test(staff_check, login_url="control_panel:panel_login")
def generic_form(request, slug, pk=None):
    entry = _get_entry(slug)
    model = entry["model"]
    Form = modelform_factory(model, exclude=entry.get("exclude", []))
    instance = get_object_or_404(model, pk=pk) if pk else None

    if request.method == "POST":
        form = Form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"{entry['label']} saved.")
            return redirect("control_panel:panel_list", slug=slug)
        messages.error(request, "Please fix the errors below.")
    else:
        form = Form(instance=instance)

    return render(request, "control_panel/form.html", {
        "entry": entry, "slug": slug, "form": form, "instance": instance,
    })


@login_required(login_url="control_panel:panel_login")
@user_passes_test(staff_check, login_url="control_panel:panel_login")
def generic_delete(request, slug, pk):
    entry = _get_entry(slug)
    obj = get_object_or_404(entry["model"], pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"{entry['label']} deleted.")
        return redirect("control_panel:panel_list", slug=slug)
    return render(request, "control_panel/confirm_delete.html", {"entry": entry, "slug": slug, "obj": obj})

ALLOWED_FILE_FIELDS = {"application_letter", "cv"}


@login_required(login_url="control_panel:panel_login")
@user_passes_test(staff_check, login_url="control_panel:panel_login")
def volunteer_file(request, pk, field):
    if field not in ALLOWED_FILE_FIELDS:
        raise Http404
    app = get_object_or_404(VolunteerApplication, pk=pk)
    f = getattr(app, field)
    if not f:
        raise Http404
    ext = os.path.splitext(f.name)[1]
    filename = f"{slugify(app.full_name)}-{field}{ext}"
    return FileResponse(f.open("rb"), filename=filename)



@login_required(login_url="control_panel:panel_login")
@require_POST
def send_record_email(request, slug, pk):
    # Only staff members can send emails from the admin panel.
    if not request.user.is_staff:
        raise PermissionDenied

    # Find the registered model for this admin page.
    entry = PANEL_REGISTRY.get(slug)

    if entry is None:
        messages.error(request, "Invalid admin section.")
        return redirect("control_panel:panel_dashboard")

    model = entry["model"]

    # Retrieve the selected database record.
    instance = get_object_or_404(model, pk=pk)

    # Ensure the record has an email field and a valid recipient.
    recipient = getattr(instance, "email", None)

    if not recipient:
        messages.error(
            request,
            "This record does not have an email address."
        )
        return redirect(
            reverse(
                "control_panel:panel_edit",
                kwargs={"slug": slug, "pk": pk},
            )
        )

    # Read and validate the submitted email content.
    subject = request.POST.get("subject", "").strip()
    message_body = request.POST.get("message", "").strip()

    if not subject or not message_body:
        messages.error(
            request,
            "Please provide both an email subject and message."
        )
        return redirect(
            reverse(
                "control_panel:panel_edit",
                kwargs={"slug": slug, "pk": pk},
            )
        )

    if len(subject) > 200:
        messages.error(
            request,
            "The email subject must not exceed 200 characters."
        )
        return redirect(
            reverse(
                "control_panel:panel_edit",
                kwargs={"slug": slug, "pk": pk},
            )
        )

    # Send the email using Django's configured email backend.
    try:
        sent = send_mail(
            subject=subject,
            message=message_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

        if sent == 1:
            messages.success(
                request,
                f"Email sent successfully to {recipient}."
            )
        else:
            messages.error(
                request,
                "The email was not sent. Please check your email settings."
            )

    except Exception:
        logger.exception(
            "Failed to send admin email for %s record %s",
            slug,
            pk,
        )
        messages.error(
            request,
            "Failed to send the email. Check your email configuration "
            "and server logs."
        )

    # Return to the record being edited.
    return redirect(
        reverse(
            "control_panel:panel_edit",
            kwargs={"slug": slug, "pk": pk},
        )
    )
