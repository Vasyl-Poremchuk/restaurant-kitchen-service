from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from restaurant.models import Cook, DishType, Dish


@login_required
def index(request):
    num_cooks = Cook.objects.count()
    num_dish_types = DishType.objects.count()
    num_dishes = Dish.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dish_types": num_dish_types,
        "num_dishes": num_dishes,
        "num_visits": num_visits + 1,
    }

    return render(request, template_name="restaurant/index.html", context=context)


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "restaurant/dish_type_list.html"
    context_object_name = "dish_type_list"
    queryset = DishType.objects.all()
    paginate_by = 5


class DishListView(generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")
    paginate_by = 5


class DishDetailView(generic.DetailView):
    model = Dish


class CookListView(generic.ListView):
    model = Cook
    paginate_by = 5


class CookDetailView(generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes__dish_type")
