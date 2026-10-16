import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.mail import send_mail
from .models import (
    Organization, TeamMember, Program, Project, Beneficiary, Partner,
    News, Event, GalleryAlbum, Document, DonationMethod, SocialLink,
    SiteSetting, Location,
)

from .forms import (
    VolunteerApplicationForm, ContactMessageForm,
    NewsletterSubscriberForm, DonationPledgeForm,
)

from django.http import HttpResponse

logger = logging.getLogger(__name__)

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "Sitemap: https://ccdo.co.tz/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")


@cache_page(60 * 15)
def home(request):
    organization = Organization.objects.first()

    active_programs = Program.objects.filter(status=Program.Status.ACTIVE).order_by("display_order")

    program_regions = (
        Location.objects.filter(programs__in=active_programs)
        .values_list("region", flat=True)
        .distinct()
    )
    regions_display = ", ".join([r for r in program_regions if r]) or None

    context = {
        "organization": organization,
        "social_links": SocialLink.objects.filter(is_active=True).order_by("display_order"),
        "site_settings": {s.key: s.value for s in SiteSetting.objects.all()},
        "regions_display": regions_display,

        "team_members": TeamMember.objects.filter(is_active=True).order_by("display_order"),

        "programs": active_programs,
        "featured_program": active_programs.filter(is_featured=True).first(),
        "featured_program_count": active_programs.filter(is_featured=True).count(),

        "projects": Project.objects.select_related("program", "location").order_by("-start_date"),
        # Requires the Project.is_featured field described in models_additions.py
        "featured_project": Project.objects.select_related("program", "location")
            .filter(is_featured=True).order_by("-start_date").first(),

        "beneficiaries": Beneficiary.objects.all(),
        "partners": Partner.objects.filter(is_active=True).order_by("display_order"),

        "news_list": News.objects.filter(status=News.Status.PUBLISHED)
            .select_related("author").order_by("-published_at")[:5],
        "events": Event.objects.select_related("location").order_by("start_datetime")[:3],

        "gallery_images": GalleryAlbum.objects.prefetch_related("images").first(),
        "documents": Document.objects.filter(is_public=True).order_by("-publication_date")[:3],

        "donation_methods": DonationMethod.objects.filter(is_active=True),

        "volunteer_form": VolunteerApplicationForm(),
        "contact_form": ContactMessageForm(),
        "newsletter_form": NewsletterSubscriberForm(),
        "donation_form": DonationPledgeForm(),
    }
    return render(request, "main/index.html", context)


def _back_to_home(request, anchor):
    referer = request.META.get("HTTP_REFERER")
    return redirect((referer or "/") + f"#{anchor}")


@require_http_methods(["POST"])
def submit_volunteer(request):
    form = VolunteerApplicationForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "Thanks, your volunteer application has been received.")
    else:
        # Show the first specific error, e.g. "File must be 5 MB or smaller."
        first_error = next(
            (err for errors in form.errors.values() for err in errors), None
        )
        messages.error(
            request,
            first_error or "Please check the form and try again.",
        )
    return _back_to_home(request, "volunteer")


@require_http_methods(["POST"])
def submit_contact(request):
    form = ContactMessageForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Your message has been sent — we'll be in touch.")
    else:
        messages.error(request, "Please check the form and try again.")
    return _back_to_home(request, "contact")



@require_http_methods(["POST"])
def submit_newsletter(request):
    form = NewsletterSubscriberForm(request.POST)

    if form.is_valid():
        subscriber = form.save()

        try:
            greeting = (
                f"Hello {subscriber.name},"
                if subscriber.name
                else "Hello,"
            )

            send_mail(
                subject="Welcome to CCDO Updates!",
                message=(
                    f"{greeting}\n\n"
                    "Thank you for subscribing to CCDO updates!\n\n"
                    "We'll keep you informed about our community "
                    "development activities, projects, and news.\n\n"
                    "We're glad to have you in our community.\n\n"
                    "Best regards,\n"
                    "CCDO Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                fail_silently=False,
            )

            messages.success(
                request,
                "You're subscribed! Please check your email "
                "for a welcome message."
            )

        except Exception:
            logger.exception(
                "Failed to send newsletter email to %s",
                subscriber.email,
            )

            messages.success(
                request,
                "You're subscribed to CCDO updates."
            )

    else:
        messages.error(
            request,
            "Please enter a valid email address."
        )

    return _back_to_home(request, "volunteer")



@require_http_methods(["POST"])
def submit_donation(request):
    form = DonationPledgeForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Thank you - your donation has been recorded. We'll be in touch to confirm.")
    else:
        messages.error(request, "Please check the donation form and try again.")
    return _back_to_home(request, "support")
