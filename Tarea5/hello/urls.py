from django.urls import path
from hello import views

urlpatterns = [
    path("", views.get_all, name="home"),
    path("poblar", views.poblar, name="poblar"),
    path("books", views.get_all, name="books"),
    path("search", views.search, name="search"),
    path("delete/<str:id>", views.delete, name="delete"),
    path("create", views.create, name="create"),
    path("get/<str:id>", views.details, name="details"),
    path("update/<str:id>", views.update, name="update"),
    path("update_data/<str:id>", views.update_data, name="update_data"),
    path("busqueda_parcial", views.busqueda_parcial, name="busqueda_parcial")
]