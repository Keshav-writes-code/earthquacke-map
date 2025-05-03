from django.urls import path
from .views import get_data, home_view


urlpatterns = [
    path("", home_view, name="home"),
    path("get_data/", get_data),
]
