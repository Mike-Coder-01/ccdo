from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.forms import modelform_factory
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .panel_registry import PANEL_REGISTRY, GROUP_ORDER


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
