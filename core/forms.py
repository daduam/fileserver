from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class SendDocumentAttachmentForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=False)
    message = forms.CharField(required=False)
