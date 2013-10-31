from django.test import TestCase
from django.contrib.auth.models import User
from sell.forms import SellOutfitForm, SellPieceForm
from django.forms import ValidationError


class SimpleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='awesome',
            email='awesome@awesome.com',
            password='password'
        )

    def test_step_one_form_with_no_outfit_pictures(self):
        data = {
            'name': 'Name of Form'
        }
        kwargs = {
            'user': self.user
        }
        form = SellOutfitForm(data, **kwargs)
        with self.assertRaises(ValidationError):
            self.assertFalse(form.clean())

    def test_step_two_form_with_no_piece_pictures(self):
        data = {
            'name': 'Name of Form'
        }
        kwargs = {
            'user': self.user
        }
        form = SellPieceForm(data, **kwargs)
        with self.assertRaises(ValidationError):
            self.assertFalse(form.clean())

    #TODO: add tests for valid cases when there are pictures saved, figure out how to create Pictures
