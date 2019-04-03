from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/', views.userList),
    path('users/<str:username>/', views.userDetail),
    path('<str:path>/', views.badRequest),
]

urlpatterns = format_suffix_patterns(urlpatterns)

