from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'control_panel'

urlpatterns = [
    path("login/", views.PanelLoginView.as_view(), name="panel_login"),
    path("logout/", LogoutView.as_view(next_page="control_panel:panel_login"), name="panel_logout"),
    path("panel_dashboard/", views.dashboard, name="panel_dashboard"),
    path("<slug:slug>/", views.generic_list, name="panel_list"),
    path("<slug:slug>/add/", views.generic_form, name="panel_add"),
    path("<slug:slug>/<int:pk>/edit/", views.generic_form, name="panel_edit"),
    path("<slug:slug>/<int:pk>/delete/", views.generic_delete, name="panel_delete"),
]
