from django.urls import path

from . import views


urlpatterns = [
    path("criar/", views.signup, name="signup"),
]
