from django import forms
from .models import VolunteerApplication, ContactMessage, NewsletterSubscriber, DonationPledge
import os

ALLOWED_DOC_EXT = {".pdf", ".doc", ".docx"}
MAX_DOC_SIZE = 5 * 1024 * 1024  # 5 MB


AREA_OF_INTEREST_CHOICES = [
    ("Community health", "Community health"),
    ("HIV/AIDS prevention", "HIV/AIDS prevention"),
    ("Environmental health & sanitation", "Environmental health & sanitation"),
    ("Communications & outreach", "Communications & outreach"),
    ("Other", "Other"),
]


def _validate_document(f):
    if f:
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ALLOWED_DOC_EXT:
            raise forms.ValidationError("Only PDF or Word files (.pdf, .doc, .docx) are allowed.")
        if f.size > MAX_DOC_SIZE:
            raise forms.ValidationError("File must be 5 MB or smaller.")
    return f


class VolunteerApplicationForm(forms.ModelForm):
    
    area_of_interest = forms.MultipleChoiceField(
        choices=AREA_OF_INTEREST_CHOICES,
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "interest-select",
        }),
    )


    application_letter = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={"accept": ".pdf,.doc,.docx"}
        ),
    )

    cv = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={"accept": ".pdf,.doc,.docx"}
        ),
    )

    class Meta:
        model = VolunteerApplication
        fields = [
            "full_name",
            "email",
            "phone",
            "area_of_interest",
            "application_letter",
            "cv",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"placeholder": "Your full name", "required": True}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "you@example.com", "required": True}
            ),
            "phone": forms.TextInput(attrs={"placeholder": "+255..."}),
        }

    def clean_area_of_interest(self):
        selected = self.cleaned_data.get("area_of_interest", [])
        return ", ".join(selected)

    def clean_application_letter(self):
        return _validate_document(
            self.cleaned_data.get("application_letter")
        )

    def clean_cv(self):
        return _validate_document(self.cleaned_data.get("cv"))

    

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "required": True}),
            "subject": forms.TextInput(attrs={"placeholder": "How can we help?", "required": True}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Write your message...", "required": True}),
        }


class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "required": True}),
        }


class DonationPledgeForm(forms.ModelForm):
    class Meta:
        model = DonationPledge
        fields = ["full_name", "email", "phone", "amount", "method"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "required": True}),
            "phone": forms.TextInput(attrs={"placeholder": "+255..."}),
            "amount": forms.NumberInput(attrs={"placeholder": "e.g. 50000", "min": "1000", "step": "500", "required": True}),
        }




