from django.db import models
from django.db import models
from django.utils.text import slugify
import uuid, os


def volunteer_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"volunteers/{uuid.uuid4().hex}{ext}"

# ---------------------------------------------------------------------------
# 1. Organization
# ---------------------------------------------------------------------------
class Organization(models.Model):
    name = models.CharField(max_length=255, default="Community Care and Development Organization")
    acronym = models.CharField(max_length=20, default="CCDO")
    description = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    established_year = models.PositiveIntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to="org/", blank=True, null=True)
    favicon = models.ImageField(upload_to="org/", blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    postal_address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.acronym or self.name

# ---------------------------------------------------------------------------
# DONATION
# ---------------------------------------------------------------------------
class DonationPledge(models.Model):
    class Method(models.TextChoices):
        VISA = "visa", "Visa"
        MASTERCARD = "mastercard", "Mastercard"
        BANK = "bank", "Bank transfer"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="TZS")
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.full_name} — {self.amount} {self.currency} ({self.status})"

# ---------------------------------------------------------------------------
# 2. Team Member
# ---------------------------------------------------------------------------
class TeamMember(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="team_members")
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    linkedin_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.position})"


# ---------------------------------------------------------------------------
# 6. Location  (defined early since Program/Project/Event reference it)
# ---------------------------------------------------------------------------
class Location(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)
    council = models.CharField(max_length=255, blank=True)
    ward = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Locations"

    def __str__(self):
        parts = [p for p in [self.ward, self.council, self.district, self.region] if p]
        return " / ".join([self.name] + parts) if parts else self.name


# ---------------------------------------------------------------------------
# 4. Program
# ---------------------------------------------------------------------------
class Program(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        UPCOMING = "upcoming", "Upcoming"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="programs")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to="programs/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    display_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    locations = models.ManyToManyField(Location, through="ProgramLocation", related_name="programs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProgramLocation(models.Model):
    """M:N join table between Program and Location."""
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("program", "location")

    def __str__(self):
        return f"{self.program} @ {self.location}"


# ---------------------------------------------------------------------------
# 5. Project
# ---------------------------------------------------------------------------
class Project(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="projects")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    featured_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    objectives = models.TextField(blank=True)
    beneficiaries = models.ManyToManyField("Beneficiary", through="ProjectBeneficiary", related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# 8. Beneficiary
# ---------------------------------------------------------------------------
class Beneficiary(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Beneficiaries"

    def __str__(self):
        return self.name


class ProjectBeneficiary(models.Model):
    """M:N join table between Project and Beneficiary."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(Beneficiary, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("project", "beneficiary")

    def __str__(self):
        return f"{self.project} - {self.beneficiary}"


# ---------------------------------------------------------------------------
# 9. Partner
# ---------------------------------------------------------------------------
class Partner(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="partners")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="partners/", blank=True, null=True)
    website = models.URLField(blank=True)
    type = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# 10. News
# ---------------------------------------------------------------------------
class News(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="news")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="news/", blank=True, null=True)
    author = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="news_articles")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# 11. Event
# ---------------------------------------------------------------------------
class Event(models.Model):
    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")
    featured_image = models.ImageField(upload_to="events/", blank=True, null=True)
    registration_required = models.BooleanField(default=False)
    registration_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPCOMING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_datetime"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# 12. Gallery
# ---------------------------------------------------------------------------
class GalleryAlbum(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="gallery_albums")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="gallery/covers/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="gallery/images/")
    caption = models.TextField(blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.alt_text or f"Image {self.pk}"


# ---------------------------------------------------------------------------
# 13. Document
# ---------------------------------------------------------------------------
class Document(models.Model):
    class DocumentType(models.TextChoices):
        ANNUAL_REPORT = "annual_report", "Annual Report"
        RESEARCH = "research", "Research"
        PUBLICATION = "publication", "Publication"
        POLICY = "policy", "Policy"
        STRATEGIC_PLAN = "strategic_plan", "Strategic Plan"
        OTHER = "other", "Other"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    document_type = models.CharField(max_length=30, choices=DocumentType.choices, default=DocumentType.OTHER)
    file = models.FileField(upload_to="documents/")
    publication_date = models.DateField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-publication_date"]

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# 14. Volunteer Application
# ---------------------------------------------------------------------------
class VolunteerApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWED = "reviewed", "Reviewed"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        CONTACTED = "contacted", "Contacted"

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=255, blank=True)
    area_of_interest = models.CharField(max_length=255, blank=True)
    experience = models.TextField(blank=True)
    motivation = models.TextField(blank=True)
    cv = models.FileField(upload_to=volunteer_upload_path, blank=True, null=True)
    application_letter = models.FileField(upload_to=volunteer_upload_path, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.full_name} ({self.status})"


# ---------------------------------------------------------------------------
# 15. Contact Message
# ---------------------------------------------------------------------------
class ContactMessage(models.Model):
    class Status(models.TextChoices):
        UNREAD = "unread", "Unread"
        READ = "read", "Read"
        REPLIED = "replied", "Replied"
        ARCHIVED = "archived", "Archived"

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNREAD)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"


# ---------------------------------------------------------------------------
# 16. Newsletter Subscriber
# ---------------------------------------------------------------------------
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


# ---------------------------------------------------------------------------
# 17. Donation Method
# ---------------------------------------------------------------------------
class DonationMethod(models.Model):
    class MethodType(models.TextChoices):
        MOBILE_MONEY = "mobile_money", "Mobile Money"
        BANK = "bank", "Bank"
        VISA = "visa", "Visa"
        MASTERCARD = "mastercard", "Mastercard"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="donation_methods")
    method_type = models.CharField(max_length=20, choices=MethodType.choices)
    provider = models.CharField(max_length=100, blank=True)
    account_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_method_type_display()} - {self.provider}"


# ---------------------------------------------------------------------------
# 18. Social Link
# ---------------------------------------------------------------------------
class SocialLink(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=100)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.platform


# ---------------------------------------------------------------------------
# 19. Site Setting
# ---------------------------------------------------------------------------
class SiteSetting(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField(blank=True)
    type = models.CharField(max_length=50, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


# ---------------------------------------------------------------------------
# 20. SEO Metadata
# ---------------------------------------------------------------------------
class SEOMetadata(models.Model):
    page_type = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)
    canonical_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "SEO Metadata"
        verbose_name_plural = "SEO Metadata"
        unique_together = ("page_type", "object_id")

    def __str__(self):
        return f"{self.page_type} #{self.object_id or '-'}"