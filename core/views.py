import mimetypes

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, DetailView, ListView

from .forms import SendDocumentAttachmentForm, SignUpForm
from .mail import send_account_verification_mail, send_file_attachment_to_email
from .models import Document, User
from .tokens import account_activation_token


class FeedView(ListView):
    model = Document
    template_name = "core/feed.html"


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "password1_help_text": form.fields["password1"].help_text,
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get("email")
            if send_account_verification_mail(request, user, email):
                messages.success(
                    request,
                    "Your account has been created successfully. Check your email for account activation link.",
                )
                return HttpResponseRedirect(reverse("login"))
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "password1_help_text": form.fields["password1"].help_text,
            },
        )


class LoginView(SuccessMessageMixin, LoginView):
    success_message = "Welcome! You have successfully logged in."


@method_decorator(login_required, name="dispatch")
class SearchResultsView(ListView):
    model = Document
    template_name = "core/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Document.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )


@method_decorator(login_required, name="dispatch")
class DocumentPreviewView(DetailView):
    model = Document


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Your account has been verified successfully! You can now log in and start using our services.",
        )
        return HttpResponseRedirect(reverse("login"))
    return HttpResponse("Activation link is invalid")


@login_required
def download_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    mime_type, _ = mimetypes.guess_type(document.file.name)
    response = HttpResponse(document.file, content_type=mime_type)
    response["Content-Disposition"] = f"attachment; filename={document.file.name}"
    document.downloads = F("downloads") + 1
    document.save()
    return response


@login_required
def send_attachment(request, document_id):
    if request.method != "POST":
        return
    form = SendDocumentAttachmentForm(request.POST)
    if form.is_valid():
        document = get_object_or_404(Document, pk=document_id)
        email = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        if send_file_attachment_to_email(
            request, email, document.file, subject, message
        ):
            messages.success(
                request,
                "An email with the file attachment has been sent successfully to the provided email address.",
            ),
            document.emails = F("emails") + 1
            document.save()
    return HttpResponseRedirect(
        reverse("core:preview_document", kwargs={"pk": document_id})
    )


@login_required
def show_pdf(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    response = HttpResponse(document.file.read(), content_type="application/pdf")
    filename = document.file.name
    response["Content-Disposition"] = f"inline; attachment; filename={filename}"
    return response
