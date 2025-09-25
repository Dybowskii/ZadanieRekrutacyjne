"""Pesel app apps."""
# Django
from django.apps import AppConfig


class PeselAppConfig(AppConfig):
    """Configuration for the PESEL Django app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pesel_app'
