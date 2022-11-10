from django.shortcuts import render

from restaurant.models import Cook, DishType, Dish


def index(request):
    num_cookers = Cook.objects.count()
    num_dish_types = DishType.objects.count()
    num_dishes = Dish.objects.count()

    context = {
        "num_cookers": num_cookers,
        "num_dish_types": num_dish_types,
        "num_dishes": num_dishes,
    }

    return render(request, template_name="restaurant/index.html", context=context)
