from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Organization,
    DonationPledge,
    TeamMember,
    Location,
    Program,
    ProgramLocation,
    Project,
    Beneficiary,
    ProjectBeneficiary,
    Partner,
    News,
    Event,
    GalleryAlbum,
    GalleryImage,
    Document,
    VolunteerApplication,
    ContactMessage,
    NewsletterSubscriber,
    DonationMethod,
    SocialLink,
    SiteSetting,
    SEOMetadata,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "acronym", "email", "phone", "registration_number")
    search_fields = ("name", "acronym", "email", "registration_number")


@admin.register(DonationPledge)
class DonationPledgeAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "amount",
        "currency",
        "method",
        "status",
        "submitted_at",
    )
    list_filter = ("method", "status")
    search_fields = ("full_name", "email", "phone")
    ordering = ("-submitted_at",)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "position",
        "organization",
        "is_active",
        "display_order",
    )
    list_filter = ("is_active", "organization")
    search_fields = ("full_name", "position", "email")
    ordering = ("display_order", "full_name")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "region",
        "district",
        "council",
        "ward",
    )
    list_filter = ("region", "district", "council")
    search_fields = (
        "name",
        "region",
        "district",
        "council",
        "ward",
    )


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "status",
        "is_featured",
        "display_order",
    )
    list_filter = ("status", "is_featured", "organization")
    search_fields = ("name", "description", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order", "name")


@admin.register(ProgramLocation)
class ProgramLocationAdmin(admin.ModelAdmin):
    list_display = ("program", "location")
    list_filter = ("program", "location")
    search_fields = ("program__name", "location__name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "program",
        "status",
        "start_date",
        "end_date",
        "is_featured",
    )
    list_filter = ("status", "is_featured", "organization", "program")
    search_fields = ("name", "summary", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-start_date",)


@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")


@admin.register(ProjectBeneficiary)
class ProjectBeneficiaryAdmin(admin.ModelAdmin):
    list_display = ("project", "beneficiary")
    list_filter = ("project", "beneficiary")
    search_fields = ("project__name", "beneficiary__name")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "type",
        "is_active",
        "display_order",
    )
    list_filter = ("is_active", "type", "organization")
    search_fields = ("name", "type", "description")
    ordering = ("display_order", "name")


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization",
        "author",
        "status",
        "published_at",
    )
    list_filter = ("status", "organization")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization",
        "start_datetime",
        "end_datetime",
        "status",
        "registration_required",
    )
    list_filter = ("status", "registration_required", "organization")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("start_datetime",)


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "created_at")
    list_filter = ("organization",)
    search_fields = ("title", "description")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = (
        "album",
        "alt_text",
        "display_order",
        "uploaded_at",
    )
    list_filter = ("album",)
    search_fields = ("alt_text", "caption")
    ordering = ("display_order",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization",
        "document_type",
        "publication_date",
        "is_public",
    )
    list_filter = ("document_type", "is_public", "organization")
    search_fields = ("title", "description")
    ordering = ("-publication_date",)


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "area_of_interest",
        "letter_link",
        "cv_link",
        "status",
        "submitted_at",
    )
    list_filter = ("status", "area_of_interest")
    list_editable = ("status",)
    search_fields = (
        "full_name",
        "email",
        "phone",
        "location",
        "area_of_interest",
    )
    ordering = ("-submitted_at",)
    readonly_fields = ("submitted_at", "letter_link", "cv_link")
    date_hierarchy = "submitted_at"

    @admin.display(description="Application letter")
    def letter_link(self, obj):
        if obj.application_letter:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">Open</a>',
                obj.application_letter.url,
            )
        return "-"

    @admin.display(description="CV")
    def cv_link(self, obj):
        if obj.cv:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">Open</a>',
                obj.cv.url,
            )
        return "-"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "status",
        "submitted_at",
    )
    list_filter = ("status",)
    search_fields = ("name", "email", "subject", "message")
    ordering = ("-submitted_at",)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name",
        "is_active",
        "subscribed_at",
        "unsubscribed_at",
    )
    list_filter = ("is_active",)
    search_fields = ("email", "name")
    ordering = ("-subscribed_at",)


@admin.register(DonationMethod)
class DonationMethodAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "method_type",
        "provider",
        "account_name",
        "is_active",
    )
    list_filter = ("method_type", "is_active", "organization")
    search_fields = (
        "provider",
        "account_name",
        "account_number",
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = (
        "platform",
        "organization",
        "url",
        "is_active",
        "display_order",
    )
    list_filter = ("is_active", "organization")
    search_fields = ("platform", "url")
    ordering = ("display_order",)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "type", "value", "updated_at")
    search_fields = ("key", "value", "type")
    ordering = ("key",)


@admin.register(SEOMetadata)
class SEOMetadataAdmin(admin.ModelAdmin):
    list_display = (
        "page_type",
        "object_id",
        "meta_title",
        "canonical_url",
    )
    list_filter = ("page_type",)
    search_fields = (
        "page_type",
        "meta_title",
        "meta_description",
        "canonical_url",
    )