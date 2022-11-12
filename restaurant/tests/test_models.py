from django.contrib.auth import get_user_model
from django.test import TestCase

from restaurant.models import DishType, Dish


class ModelsTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(
            name="Jellies",
        )

        self.assertEqual(
            str(dish_type),
            dish_type.name,
        )

    def test_cook_str(self):
        cook = get_user_model().objects.create_user(
            username="bob.beamon",
            password="supercook123",
            first_name="Bob",
            last_name="Beamon",
        )

        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})",
        )

    def test_dish_str(self):
        dish_type = DishType.objects.create(
            name="Leftovers",
        )
        dish = Dish.objects.create(
            name="PORK AND APPLE RISSOLES WITH SPICED APPLE SAUCE",
            description="These can be made with leftover cooked pork "
                        "from a joint or the ready minced raw pork "
                        "which is now widely available.",
            price=105.5,
            dish_type=dish_type,
        )

        self.assertEqual(str(dish), dish.name)

    def test_create_cook_with_years_of_experience(self):
        username = "michael.jordan"
        password = "dude112345"
        years_of_experience = 7

        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience,
        )

        self.assertEqual(cook.username, username)
        self.assertTrue(cook.check_password(password))
        self.assertEqual(cook.years_of_experience, years_of_experience)

    def test_cook_get_absolute_url(self):
        cook = get_user_model().objects.create_user(
            username="michael.phelps",
            password="supercook123",
            first_name="Michael",
            last_name="Phelps",
        )

        self.assertEqual(cook.get_absolute_url(), "/cooks/1/")
