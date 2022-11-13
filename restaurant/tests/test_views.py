from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from restaurant.models import DishType, Dish

DISH_TYPE_LIST_URL = reverse("restaurant:dish-type-list")
DISH_TYPE_CREATE_URL = reverse("restaurant:dish-type-create")
DISH_LIST_URL = reverse("restaurant:dish-list")


class PublicDishTypeTest(TestCase):
    def test_login_required_list(self) -> None:
        response = self.client.get(DISH_TYPE_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_create(self) -> None:
        response = self.client.get(DISH_TYPE_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDishTypeTests(TestCase):
    def setUp(self) -> None:
        self.cook = get_user_model().objects.create_user(
            username="tom.cruise",
            password="cruisecook123",
            first_name="Tom",
            last_name="Cruise",
        )
        self.client.force_login(self.cook)

    def test_retrieve_dish_types(self) -> None:
        DishType.objects.create(
            name="Pastry",
        )
        DishType.objects.create(
            name="Risotto and Gnocchi",
        )

        response = self.client.get(DISH_TYPE_LIST_URL)
        dish_types = DishType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types),
        )
        self.assertTemplateUsed(
            response, "restaurant/dish_type_list.html",
        )

    def test_login_required_update(self) -> None:
        dish_type = DishType.objects.create(
            name="Soups",
        )
        dish_type_update_url = reverse(
            "restaurant:dish-type-update", args=[dish_type.pk],
        )
        response = self.client.post(dish_type_update_url)
        self.assertEqual(response.status_code, 200)

    def test_login_required_deleted(self) -> None:
        dish_type = DishType.objects.create(
            name="Souffles",
        )
        dish_type_delete_url = reverse(
            "restaurant:dish-type-delete",
            args=[dish_type.pk],
        )
        response = self.client.post(dish_type_delete_url)

        self.assertEqual(response.status_code, 302)

    def test_dish_type_search(self) -> None:
        search_form = "Tarts and Flans"
        dish_type_search = DishType.objects.create(
            name=search_form,
        )
        dish_types = (
            "Stir-fry", "Sunday roast",
            "Summer soup", "Pastry",
            "Risotto and Gnocchi",
        )
        for dish_type in dish_types:
            DishType.objects.create(
                name=dish_type,
            )
        response = self.client.get(
            f"{DISH_TYPE_LIST_URL}?name={search_form}"
        )

        self.assertEqual(
            response.context["dish_type_list"].count(), 1,
        )
        self.assertEqual(
            response.context["dish_type_list"][0],
            dish_type_search,
        )


class PrivateCookTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="tom.hanks",
            password="actor12345",
        )
        self.client.force_login(self.user)

    def test_create_cook(self) -> None:
        form_data = {
            "username": "kobe.bryant",
            "password1": "kobecook123",
            "password2": "kobecook123",
            "years_of_experience": 9,
            "first_name": "Kobe",
            "last_name": "Bryant",
        }
        self.client.post(reverse(
            "restaurant:cook-create"), data=form_data,
        )
        response = self.client.get(
            reverse("restaurant:cook-list"),
        )
        new_cook = get_user_model().objects.get(
            username=form_data["username"],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_cook.first_name, form_data["first_name"])
        self.assertEqual(new_cook.last_name, form_data["last_name"])
        self.assertEqual(
            new_cook.years_of_experience, form_data["years_of_experience"]
        )


class PrivateDishTests(TestCase):
    def setUp(self) -> None:
        self.cook = get_user_model().objects.create_user(
            username="tom.cruise",
            password="cruisecook123",
            first_name="Tom",
            last_name="Cruise",
        )
        self.client.force_login(self.cook)

    def test_retrieve_dishes(self) -> None:
        dish_type = DishType.objects.create(
            name="Pastry",
        )
        dish = Dish.objects.create(
            name="APPLE AND BLACKBERRY PIE",
            description="This is best of all made with wild brambles, "
                        "which seem to have twice as much flavour as "
                        "the cultivated kind.",
            price=74.5,
            dish_type=dish_type
        )

        response = self.client.get(DISH_LIST_URL)
        dishes = Dish.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes),
        )
        self.assertTemplateUsed(
            response, "restaurant/dish_list.html",
        )

    def test_login_required_update(self) -> None:
        dish_type = DishType.objects.create(
            name="Pastry",
        )
        dish = Dish.objects.create(
            name="APRICOT GALETTES WITH AMARETTO",
            description="Galettes are very thin discs of flaky "
                        "pastry which have no sides, the pastry "
                        "is barely there, yet it gives a light, "
                        "very crisp background to all kinds of "
                        "toppings, both savoury and sweet.",
            price=80.0,
            dish_type=dish_type
        )
        dish_update_url = reverse(
            "restaurant:dish-update", args=[dish.pk],
        )
        response = self.client.post(dish_update_url)
        self.assertEqual(response.status_code, 200)

    def test_login_required_deleted(self) -> None:
        dish_type = DishType.objects.create(
            name="Pastry",
        )
        dish = Dish.objects.create(
            name="PICNIC PORK PIE",
            description="The reason this pie is great for a picnic is "
                        "that it stays beautifully moist and is so "
                        "easy to slice and serve.",
            price=83.0,
            dish_type=dish_type
        )
        dish_delete_url = reverse("restaurant:dish-list")
        response = self.client.post(dish_delete_url)

        self.assertEqual(response.status_code, 405)

    def test_dish_search(self) -> None:
        dish_type = DishType.objects.create(
            name="Dishes",
        )
        search_form = "PUMPKIN PIE"
        dish_search = Dish.objects.create(
            name=search_form,
            description="It's richer than shortcrust, but very "
                        "crisp, and the eggs give it a shortbread "
                        "quality. Nuts can sometimes be added; here "
                        "there are toasted pecans, although walnuts or "
                        "hazelnuts can be used, or the pastry can "
                        "be made without nuts if you prefer.",
            price=65.5,
            dish_type=dish_type,
        )
        dishes = (
            {
                "name": "CHINESE CRISPY BEEF STIR-FRY",
                "description": "The good thing about Chinese cooking "
                               "is that it always manages to make a "
                               "little meat go a long way.",
                "price": 96.0,
            },
            {
                "name": "AUTUMN LAMB BRAISED IN BEAUJOLAIS",
                "description": "This is certainly one of the best ways "
                               "to cook lamb in the autumn or winter months "
                               "– slowly braising it under a tent of foil "
                               "keeps it beautifully moist and really seems "
                               "to develop its full flavour.",
                "price": 125.5,
            },
            {
                "name": "CHILLED SPANISH GAZPACHO",
                "description": "This is a truly beautiful soup for serving "
                               "ice-cold during the summer and it's particularly "
                               "refreshing if we're lucky enough to have hot weather.",
                "price": 88.5,
            }
        )
        for dish in dishes:
            Dish.objects.create(
                name=dish["name"],
                description=dish["description"],
                price=dish["price"],
                dish_type=dish_type
            )
        response = self.client.get(
            f"{DISH_LIST_URL}?name={search_form}"
        )

        self.assertEqual(
            response.context["dish_list"].count(), 1,
        )
        self.assertEqual(
            response.context["dish_list"][0],
            dish_search,
        )
