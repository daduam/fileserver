from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import generic

from .forms import SignUpForm
from .mail import send_account_verification_mail
from .models import User
from .tokens import account_activation_token


class SignUpView(generic.CreateView):
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
            send_account_verification_mail(request, user, email)
            return HttpResponseRedirect(reverse("login"))
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "password1_help_text": form.fields["password1"].help_text,
            },
        )


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse("login"))
    return HttpResponse("Activation link is invalid")
