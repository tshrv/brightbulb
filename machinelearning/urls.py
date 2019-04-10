from django.urls import path
from . import views

urlpatterns = [
    path('weatherforecast/<str:date_str>/', views.make_prediction),
    path('weatherforecast/', views.description),
]
