from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from restaurant.forms import (
    CookCreationForm,
    CookYearsOfExperienceUpdateForm,
    DishForm,
)
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


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "restaurant/dish_type_list.html"
    context_object_name = "dish_type_list"
    queryset = DishType.objects.all()
    paginate_by = 5


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "restaurant/dish_type_form.html"
    context_object_name = "dish_type_list"
    fields = "__all__"
    success_url = reverse_lazy("restaurant:dish_type_list")


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "restaurant/dish_type_form.html"
    context_object_name = "dish_type_list"
    fields = "__all__"
    success_url = reverse_lazy("restaurant:dish_type_list")


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "restaurant/dish_type_confirm_delete.html"
    context_object_name = "dish_type_list"
    success_url = reverse_lazy("restaurant:dish_type_list")


class DishListView(generic.ListView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type")
    paginate_by = 5


class DishDetailView(generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("restaurant:dish_list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("restaurant:dish_list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("restaurant:dish_list")


class CookListView(generic.ListView):
    model = Cook
    paginate_by = 5


class CookDetailView(generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes__dish_type")


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookYearsOfExperienceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookYearsOfExperienceUpdateForm
    success_url = reverse_lazy("restaurant:cook_list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("restaurant:cook_list")


@login_required
def assign_driver(request, pk):
    driver = Cook.objects.get(id=request.user.id)
    if Dish.objects.get(id=pk) in driver.cars.all():
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)
    return redirect("restaurant:dish_detail", pk=pk)
