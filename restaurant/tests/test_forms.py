from django.test import TestCase

from restaurant.forms import CookCreationForm, CookYearsOfExperienceUpdateForm


class FormsTests(TestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "peter.pan",
            "password1": "prop1234",
            "password2": "prop1234",
            "first_name": "Peter",
            "last_name": "Pan",
            "years_of_experience": 3,
        }

    def test_cook_creation(self):
        form = CookCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_cook_years_of_experience_update_form(self):
        self.form_data = {
            "years_of_experience": "5",
        }
        form = CookYearsOfExperienceUpdateForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)
