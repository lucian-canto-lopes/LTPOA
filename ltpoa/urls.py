from django.contrib import admin
from django.urls import include, path

from catalog import views as catalog_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("conta/", include("accounts.urls")),
    path("conta/", include("django.contrib.auth.urls")),
    path("", catalog_views.home, name="home"),
    path("", include("catalog.urls")),
]
