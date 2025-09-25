"""Text processor tests."""
# Standard Library
import io

# Django
from django.test import TestCase
from django.urls import reverse

# Local
from .utils import reverse_word


class ReverseWordTests(TestCase):
    """Tests for reverse_word utility."""

    def test_short_words_remain_unchanged(self):
        """Words with <=3 letters stay the same."""
        self.assertEqual(reverse_word('a'), 'a')
        self.assertEqual(reverse_word('to'), 'to')
        self.assertEqual(reverse_word('kot'), 'kot')

    def test_first_and_last_character_stay_the_same(self):
        """First and last characters are preserved."""
        word = 'python'
        result = reverse_word(word)
        self.assertEqual(result[0], 'p')
        self.assertEqual(result[-1], 'n')

    def test_inner_characters_are_permuted(self):
        """Middle characters are shuffled but preserved."""
        word = 'python'
        result = reverse_word(word)
        original_middle = sorted(word[1:-1])
        shuffled_middle = sorted(result[1:-1])
        self.assertEqual(original_middle, shuffled_middle)


class TextFileFormTests(TestCase):
    """Tests for file upload form view."""

    def test_form_renders_correctly(self):
        """Form page loads with correct label."""
        response = self.client.get(reverse('text_processor:text_file_form'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Umieść plik (.txt)')

    def test_upload_valid_txt_file(self):
        """Valid .txt file is accepted and processed."""
        file_content = b'Hello World'
        txt_file = io.BytesIO(file_content)
        txt_file.name = 'example.txt'

        response = self.client.post(
            reverse('text_processor:text_file_form'),
            {'file': txt_file},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'text_processor/processed_text.html')
        self.assertContains(response, 'H')
        self.assertContains(response, 'W')

    def test_upload_empty_file_rejected(self):
        """Empty file is rejected."""
        empty_file = io.BytesIO(b'')
        empty_file.name = 'empty.txt'

        response = self.client.post(
            reverse('text_processor:text_file_form'),
            {'file': empty_file},
        )
        self.assertContains(response, 'Plik jest pusty.')

    def test_upload_invalid_extension_rejected(self):
        """File with wrong extension is rejected."""
        bad_file = io.BytesIO(b'Some content')
        bad_file.name = 'not_a_text.pdf'

        response = self.client.post(
            reverse('text_processor:text_file_form'),
            {'file': bad_file},
        )
        self.assertContains(response, 'Zły typ pliku (umieść plik z rozszerzeniem .txt)')


class ProcessedFileViewTests(TestCase):
    """Tests for processed text view."""

    def test_processed_view_without_content_in_session(self):
        """Shows info if no content in session."""
        response = self.client.get(reverse('text_processor:processed_file'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Brak zawartości do przetworzenia.')

    def test_processed_view_with_content_in_session(self):
        """Processes uploaded content from session."""
        session = self.client.session
        session['uploaded_content'] = 'Ala ma kota'
        session.save()

        response = self.client.get(reverse('text_processor:processed_file'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A')
        self.assertContains(response, 'a')
