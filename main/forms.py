from django import forms
from .models import VolunteerApplication, ContactMessage, NewsletterSubscriber, DonationPledge


AREA_OF_INTEREST_CHOICES = [
    ("Community health", "Community health"),
    ("HIV/AIDS prevention", "HIV/AIDS prevention"),
    ("Environmental health & sanitation", "Environmental health & sanitation"),
    ("Communications & outreach", "Communications & outreach"),
    ("Other", "Other"),
]


class VolunteerApplicationForm(forms.ModelForm):
    area_of_interest = forms.ChoiceField(choices=AREA_OF_INTEREST_CHOICES, required=False)

    class Meta:
        model = VolunteerApplication
        fields = ["full_name", "email", "phone", "area_of_interest"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "required": True}),
            "phone": forms.TextInput(attrs={"placeholder": "+255..."}),
        }


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
