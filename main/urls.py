from django.urls import path
from . import views


app_name = "main"


urlpatterns = [
    path("", views.home, name="home"),
    path("volunteer/submit/", views.submit_volunteer, name="submit_volunteer"),
    path("contact/submit/", views.submit_contact, name="submit_contact"),
    path("newsletter/submit/", views.submit_newsletter, name="submit_newsletter"),
    path("donate/submit/", views.submit_donation, name="submit_donation"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
