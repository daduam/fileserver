from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path("", views.FeedView.as_view(), name="feed"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "activate/<uidb64>/<token>/",
        views.activate_account,
        name="activate",
    ),
    path(
        "documents/<int:document_id>/download/",
        views.download_document,
        name="download_document",
    ),
    path(
        "documents/<pk>/preview/",
        views.DocumentPreviewView.as_view(),
        name="preview_document",
    ),
    path(
        "documents/<int:document_id>/send_attachment/",
        views.send_attachment,
        name="send_attachment",
    ),
    path(
        "search/",
        views.SearchResultsView.as_view(),
        name="search_results",
    ),
]
