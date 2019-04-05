from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # GET_ALL_USERS, ADD_NEW_USER
    path('users/', views.user_list),

    # GET_SPECIFIC_USER, UPDATE_SPECIFIC_USER, DELETE_SPECIFIC_USER
    path('users/<str:username>/', views.user_detail),

    path('<str:path>/', views.bad_request),
]

urlpatterns = format_suffix_patterns(urlpatterns)

