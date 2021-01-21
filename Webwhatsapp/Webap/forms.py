import re

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import ugettext_lazy as _

from .models import *

regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


class CreateUserForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"), widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input100 form-control'}),
        required=True)

    first_name = forms.CharField(label=_("First name"), max_length=30,
                                 widget=forms.TextInput(
                                     attrs={'placeholder': 'First name', 'class': 'input100 form-control'}),
                                 required=True
                                 )
    last_name = forms.CharField(label=_("Last name"), max_length=30,
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Last name', 'class': 'input100 form-control'}), required=True
                                )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input100 form-control'}), required=True
    )

    def clean_first_name(self):
        if (regex.search(self.cleaned_data["first_name"]) != None):
            raise forms.ValidationError(
                _("First Name cannot contain special characters."))
        else:
            return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if (regex.search(self.cleaned_data["last_name"]) != None):
            raise forms.ValidationError(
                _("Last Name cannot contain special characters."))
        else:
            return self.cleaned_data["last_name"]

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = User.objects.filter(email__iexact=value)
        if not qs.exists():
            return value
        raise forms.ValidationError(
            _("A user is registered with this email address."))


class PhoneForm(forms.Form):
    class Meta:
        model = PhoneNumber
        fields = ('phone_number',)