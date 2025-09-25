"""Pesel app views."""
# Django
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView

# Local
from .forms import PeselForm
from .utils import decode_pesel


class PeselFormView(FormView):
    """Form view for submitting and storing PESEL in session."""

    form_class = PeselForm
    template_name = 'pesel_app/main_page.html'
    success_url = reverse_lazy('pesel_app:pesel_detail')

    def form_valid(self, form):
        """Store the PESEL from the form in the session before continuing."""
        self.request.session['pesel'] = form.cleaned_data['pesel']
        return super().form_valid(form)


class PeselDetailView(TemplateView):
    """Detail view for displaying decoded PESEL information."""

    template_name = 'pesel_app/detail_page.html'

    def get_context_data(self, **kwargs):
        """Add PESEL and decoded birth date and gender to the context."""
        context = super().get_context_data(**kwargs)
        pesel = self.request.session.get('pesel')
        if pesel:
            decoded = decode_pesel(pesel)
            context['pesel'] = pesel
            if decoded:
                context['birth_date'] = decoded['birth_date']
                context['gender'] = decoded['gender']
            else:
                context['birth_date'] = 'Niepoprawny PESEL'
                context['gender'] = 'Nieznana'
        return context
