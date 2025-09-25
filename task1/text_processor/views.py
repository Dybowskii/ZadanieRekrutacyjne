"""Text processor views."""
# Standard Library
import re

# Django
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView

# Local
from .forms import TextFileForm
from .utils import reverse_word


class TextFileFormView(FormView):
    """Form view for uploading and storing text file content."""

    template_name = 'text_processor/main_page.html'
    form_class = TextFileForm
    success_url = reverse_lazy('text_processor:processed_file')

    def form_valid(self, form):
        """Save uploaded file content in session."""
        uploaded_file = form.cleaned_data['file']
        content = uploaded_file.read().decode('utf-8')
        self.request.session['uploaded_content'] = content
        return super().form_valid(form)


class ProcessedFileView(TemplateView):
    """View for displaying processed version of uploaded text."""

    template_name = 'text_processor/processed_text.html'

    def get_context_data(self, **kwargs):
        """Add processed text to template context."""
        context = super().get_context_data(**kwargs)
        content = self.request.session.get('uploaded_content')
        print(content)
        if not content:
            print('tak')
            context['processed_text'] = 'Brak zawartości do przetworzenia.'
            return context

        words = re.findall(r'\w+|\s+|[^\w\s]+', content)
        processed_text = ''.join(
            [reverse_word(word) if word.strip().isalnum() else word for word in words]
        )
        context['processed_text'] = processed_text
        return context
