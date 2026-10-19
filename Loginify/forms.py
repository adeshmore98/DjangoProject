
from django import forms
from .models import UserDetails


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data["username"]

        if UserDetails.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if UserDetails.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already registered.")

        return email


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
