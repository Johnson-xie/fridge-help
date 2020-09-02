from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'temperatures/', views.get_temperature, name='temperature-trend'),
    path(r'power/', views.get_power, name='power-trend'),
]
