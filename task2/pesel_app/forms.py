"""Pesel app forms."""
# Django
from django import forms
from django.core.exceptions import ValidationError


class PeselForm(forms.Form):
    """Form for validating a PESEL number."""

    pesel = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'placeholder': 'np. 00000000000',
            'class': 'form-control'
        })
    )

    def clean_pesel(self):
        """Validate that the PESEL is 11 digits and has a correct checksum."""
        pesel = self.cleaned_data['pesel']

        if len(pesel) != 11:
            raise ValidationError('PESEL musi mieć dokładnie 11 cyfr')

        if not pesel.isdigit():
            raise ValidationError('PESEL może zawierać tylko cyfry.')

        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        control_sum = sum(int(pesel[i]) * weights[i] for i in range(10))
        control_digit = (10 - (control_sum % 10)) % 10

        if control_digit != int(pesel[-1]):
            raise ValidationError('Nieprawidłowa suma kontrolna peselu')

        return pesel
