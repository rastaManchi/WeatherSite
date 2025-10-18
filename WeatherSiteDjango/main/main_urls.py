from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('get_month_temp', views.get_month_temp)
]