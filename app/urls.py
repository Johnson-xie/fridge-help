from django.contrib import admin
from django.urls import path
import app.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('link/', views.link),
    path('send/', views.send),
    path('to_sendmsg/', views.to_recmsg),
    path('to_recmsg/', views.to_sendmsg),
]
