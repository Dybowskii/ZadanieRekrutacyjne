"""Pesel app tests."""
# Django
from django.test import TestCase
from django.urls import reverse

# Local
from .forms import PeselForm
from .views import decode_pesel


class PeselFormTests(TestCase):
    """Tests for PeselForm validation."""

    def test_valid_pesel(self):
        """Form accepts a valid PESEL."""
        form = PeselForm(data={'pesel': '44051401458'})
        self.assertTrue(form.is_valid())

    def test_invalid_length_pesel(self):
        """Form rejects PESEL with incorrect length."""
        form = PeselForm(data={'pesel': '123'})
        self.assertFalse(form.is_valid())
        self.assertIn('PESEL musi mieć dokładnie 11 cyfr', form.errors['pesel'])

    def test_invalid_characters_pesel(self):
        """Form rejects PESEL containing non-digit characters."""
        form = PeselForm(data={'pesel': 'abcdefghijk'})
        self.assertFalse(form.is_valid())
        self.assertIn('PESEL może zawierać tylko cyfry.', form.errors['pesel'])

    def test_invalid_control_digit(self):
        """Form rejects PESEL with invalid control digit."""
        form = PeselForm(data={'pesel': '44051401459'})
        self.assertFalse(form.is_valid())
        self.assertIn('Nieprawidłowa suma kontrolna peselu', form.errors['pesel'])


class PeselFormViewTests(TestCase):
    """Tests for PeselFormView behavior."""

    def test_form_submission_saves_to_session_and_redirects(self):
        """Submitting the form saves PESEL in session and redirects."""
        url = reverse('pesel_app:pesel_form')
        response = self.client.post(url, data={'pesel': '44051401458'})
        self.assertRedirects(response, reverse('pesel_app:pesel_detail'))
        session = self.client.session
        self.assertEqual(session['pesel'], '44051401458')


class PeselDetailViewTests(TestCase):
    """Tests for PeselDetailView context data."""

    def test_context_contains_decoded_pesel(self):
        """View context contains decoded PESEL information."""
        session = self.client.session
        session['pesel'] = '44051401458'
        session.save()
        url = reverse('pesel_app:pesel_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pesel'], '44051401458')
        self.assertEqual(response.context['birth_date'], '1944-05-14')
        self.assertEqual(response.context['gender'], 'Mężczyzna')

    def test_context_invalid_pesel(self):
        """View context handles invalid PESEL correctly."""
        session = self.client.session
        session['pesel'] = '12345678901'
        session.save()
        url = reverse('pesel_app:pesel_detail')
        response = self.client.get(url)
        self.assertEqual(response.context['birth_date'], 'Niepoprawny PESEL')
        self.assertEqual(response.context['gender'], 'Nieznana')


class DecodePeselTests(TestCase):
    """Tests for the decode_pesel function."""

    def test_decode_valid_pesel(self):
        """decode_pesel returns correct date and gender for valid PESEL."""
        result = decode_pesel('44051401458')
        self.assertEqual(result['birth_date'], '1944-05-14')
        self.assertEqual(result['gender'], 'Mężczyzna')

    def test_decode_invalid_pesel_length(self):
        """decode_pesel returns None for PESEL with invalid length."""
        self.assertIsNone(decode_pesel('123'))

    def test_decode_invalid_pesel_characters(self):
        """decode_pesel returns None for PESEL containing non-digits."""
        self.assertIsNone(decode_pesel('abcdefghijk'))

    def test_decode_invalid_date(self):
        """decode_pesel returns None for PESEL with impossible date."""
        self.assertIsNone(decode_pesel('44053201458'))
