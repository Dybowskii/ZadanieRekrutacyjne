"""Text processor apps."""
# Django
from django.apps import AppConfig


class TextProcessorConfig(AppConfig):
    """Configuration for the text_processor app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'text_processor'
