from main.models import (
    Organization, TeamMember, Program, Project, Location, Beneficiary,
    Partner, News, Event, GalleryAlbum, GalleryImage, Document,
    DonationMethod, SocialLink, SiteSetting, SEOMetadata,
    VolunteerApplication, ContactMessage, NewsletterSubscriber, DonationPledge,
)

# One entry per manageable table. "group" controls sidebar grouping.
# "readonly_create": True hides the "Add new" button for tables that should
# only ever be populated by public-facing forms (volunteer/contact/newsletter/
# donation submissions) — admins can still edit (e.g. change status) and delete.
# "singleton": True means there's only ever one row (Organization) — the list
# view skips straight to editing that row.
PANEL_REGISTRY = {
    "organization": {
        "model": Organization, "label": "Organization", "group": "Site",
        "list_fields": ["name", "acronym", "email", "phone"],
        "exclude": ["created_at", "updated_at"],
        "singleton": True,
    },
    "team-members": {
        "model": TeamMember, "label": "Team Members", "group": "Content",
        "list_fields": ["full_name", "position", "is_active", "display_order"],
        "exclude": ["created_at", "updated_at"],
    },
    "programs": {
        "model": Program, "label": "Programs", "group": "Content",
        "list_fields": ["name", "status", "is_featured", "display_order"],
        "exclude": ["slug", "created_at", "updated_at"],
    },
    "projects": {
        "model": Project, "label": "Projects", "group": "Content",
        "list_fields": ["name", "program", "status", "start_date"],
        "exclude": ["slug", "created_at", "updated_at"],
    },
    "locations": {
        "model": Location, "label": "Locations", "group": "Content",
        "list_fields": ["name", "region", "district", "ward"],
        "exclude": [],
    },
    "beneficiaries": {
        "model": Beneficiary, "label": "Beneficiaries", "group": "Content",
        "list_fields": ["name"],
        "exclude": [],
    },
    "partners": {
        "model": Partner, "label": "Partners", "group": "Content",
        "list_fields": ["name", "type", "is_active", "display_order"],
        "exclude": [],
    },
    "news": {
        "model": News, "label": "News", "group": "Content",
        "list_fields": ["title", "status", "published_at"],
        "exclude": ["slug", "created_at", "updated_at"],
    },
    "events": {
        "model": Event, "label": "Events", "group": "Content",
        "list_fields": ["title", "start_datetime", "status"],
        "exclude": ["slug", "created_at", "updated_at"],
    },
    "gallery-albums": {
        "model": GalleryAlbum, "label": "Gallery Albums", "group": "Media",
        "list_fields": ["title"],
        "exclude": ["created_at"],
    },
    "gallery-images": {
        "model": GalleryImage, "label": "Gallery Images", "group": "Media",
        "list_fields": ["album", "caption", "display_order"],
        "exclude": ["uploaded_at"],
    },
    "documents": {
        "model": Document, "label": "Documents", "group": "Media",
        "list_fields": ["title", "document_type", "is_public", "publication_date"],
        "exclude": ["created_at"],
    },
    "donation-methods": {
        "model": DonationMethod, "label": "Donation Methods", "group": "Site",
        "list_fields": ["method_type", "provider", "is_active"],
        "exclude": [],
    },
    "social-links": {
        "model": SocialLink, "label": "Social Links", "group": "Site",
        "list_fields": ["platform", "url", "is_active", "display_order"],
        "exclude": [],
    },
    "site-settings": {
        "model": SiteSetting, "label": "Site Settings", "group": "Site",
        "list_fields": ["key", "value"],
        "exclude": ["updated_at"],
    },
    "seo-metadata": {
        "model": SEOMetadata, "label": "SEO Metadata", "group": "Site",
        "list_fields": ["page_type", "object_id", "meta_title"],
        "exclude": [],
    },
    "volunteer-applications": {
        "model": VolunteerApplication, "label": "Volunteer Applications", "group": "Submissions",
        "list_fields": ["full_name", "email", "area_of_interest", "status", "submitted_at"],
        "exclude": ["submitted_at"],
        "readonly_create": True,
    },
    "contact-messages": {
        "model": ContactMessage, "label": "Contact Messages", "group": "Submissions",
        "list_fields": ["name", "email", "subject", "status", "submitted_at"],
        "exclude": ["submitted_at"],
        "readonly_create": True,
    },
    "newsletter-subscribers": {
        "model": NewsletterSubscriber, "label": "Newsletter Subscribers", "group": "Submissions",
        "list_fields": ["email", "name", "is_active", "subscribed_at"],
        "exclude": ["subscribed_at", "unsubscribed_at"],
        "readonly_create": True,
    },
    "donation-pledges": {
        "model": DonationPledge, "label": "Donation Pledges", "group": "Submissions",
        "list_fields": ["full_name", "amount", "method", "status", "submitted_at"],
        "exclude": ["submitted_at"],
        "readonly_create": True,
    },
}

GROUP_ORDER = ["Site", "Content", "Media", "Submissions"]
