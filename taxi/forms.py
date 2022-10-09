from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, DecimalValidator

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number",
            "first_name",
            "last_name",
        )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class DriverLicenseUpdateForm(forms.ModelForm):
    LENGTH_LICENSE_NUMBER = 8

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != DriverLicenseUpdateForm.LENGTH_LICENSE_NUMBER:
            raise ValidationError(
                f"License number must consist only of "
                f"{DriverLicenseUpdateForm.LENGTH_LICENSE_NUMBER} characters"
            )
        for char in license_number[:3]:
            if ord(char) < 65 or ord(char) > 90:
                raise ValidationError("First 3 characters must be uppercase letters")

        for char in license_number[3:]:
            if ord(char) < 48 or ord(char) > 57:
                raise ValidationError("Last 5 characters must be digits")

        return license_number