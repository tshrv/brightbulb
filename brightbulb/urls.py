from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # GET_AUTH_TOKEN
    path('auth/', obtain_auth_token, name='auth'),

    # GET_ALL_USERS
    path('users/', views.user_list),

    # ADD_NEW_USER
    path('users/register/', views.user_register),

    # GET_UPDATE_DELETE_SPECIFIC_USER
    path('users/<str:username>/', views.user_detail),

    # GET_ALL_NOTES
    path('notes/', views.note_list_create),

    # GET_UPDATE_DELETE_SPECIFIC_NOTE
    path('notes/<str:slug>/', views.note_detail),

    path('<str:path>/', views.bad_request),
]

urlpatterns = format_suffix_patterns(urlpatterns)

