from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'api/temperatures/', views.get_temperature, name='temperature-data'),
    path(r'api/power/', views.get_power, name='power-data'),
    path(r'example/', views.index, name='example'),
    path(r'power/', views.draw_power, name='draw-power')

]
