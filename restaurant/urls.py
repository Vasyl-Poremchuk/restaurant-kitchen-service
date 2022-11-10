from django.urls import path

from restaurant.views import index, DishTypeListView, DishListView, DishDetailView, CookListView, CookDetailView

urlpatterns = [
    path("", index, name="index"),
    path(
        "dish_types/",
        DishTypeListView.as_view(),
        name="dish-type-list",
    ),
    path(
        "dishes/",
        DishListView.as_view(),
        name="dish-list",
    ),
    path(
        "dishes/<int:pk>/",
        DishDetailView.as_view(),
        name="dish-detail",
    ),
    path(
        "cookers/",
        CookListView.as_view(),
        name="cook-list",
    ),
    path(
        "cookers/<int:pk>",
        CookDetailView.as_view(),
        name="cook-detail",
    ),
]

app_name = "restaurant"
