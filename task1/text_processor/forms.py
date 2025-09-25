"""Text processor forms."""
# Django
from django import forms


class TextFileForm(forms.Form):
    """Form to upload a non-empty .txt file."""

    file = forms.FileField(
        label='Umieść plik (.txt)',
        error_messages={
            'empty': 'Plik jest pusty. Upewnij się, że zawiera jakąś treść.',
        }
    )

    def clean_file(self):
        """Validate that the uploaded file is non-empty and has a .txt extension."""
        file = self.cleaned_data['file']
        if file.size == 0:
            raise forms.ValidationError(
                'Plik nie może być pusty.'
            )
        if not file.name.endswith('.txt'):
            raise forms.ValidationError(
                'Zły typ pliku (umieść plik z rozszerzeniem .txt)'
            )
        return file
