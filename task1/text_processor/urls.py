"""Text processor utils."""
# Django
from django.urls import path

# Local
from .views import ProcessedFileView
from .views import TextFileFormView

app_name = 'text_processor'

urlpatterns = [
    path('', TextFileFormView.as_view(), name='text_file_form'),
    path('processed-file/', ProcessedFileView.as_view(), name='processed_file'),
]
