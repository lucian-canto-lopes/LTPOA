from django.urls import path

from . import views


urlpatterns = [
    path("painel/", views.dashboard, name="dashboard"),
    path("amostras/", views.sample_list, name="sample_list"),
    path("amostras/nova/", views.sample_create, name="sample_create"),
    path("amostras/<int:pk>/", views.sample_detail, name="sample_detail"),
    path("amostras/<int:pk>/editar/", views.sample_update, name="sample_update"),
]
