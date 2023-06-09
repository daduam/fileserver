from django.urls import path
from django.views.generic.base import TemplateView

from .views import SignUpView


app_name = "core"

urlpatterns = [
    path("", TemplateView.as_view(template_name="core/feed.html"), name="feed"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
