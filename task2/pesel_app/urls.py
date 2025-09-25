"""Pesel app urls."""
# Django
from django.urls import path

# Local
from .views import PeselDetailView
from .views import PeselFormView

app_name = 'pesel_app'

urlpatterns = [
    path('', PeselFormView.as_view(), name='pesel_form'),
    path('pesel-detail/', PeselDetailView.as_view(), name='pesel_detail'),
]
