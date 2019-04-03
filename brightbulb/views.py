# django
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# rest_framework
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# models
from django.contrib.auth.models import User

# serializers
from .serializers import UserSerializer


# @api_view(['GET', 'POST'])
@csrf_exempt
def userList(request, format=None):
    if request.method == 'GET':
        serializer = UserSerializer(User.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            # vulnerable: raw password being saved initially
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        else:
            content = {
                'status': status.HTTP_406_NOT_ACCEPTABLE,
                'data': request.POST,
                'error': serializer.errors,
            }
            return JsonResponse(content, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)

    # elif request.method == 'PUT':
    #     content = {
    #         'status': status.HTTP_405_METHOD_NOT_ALLOWED,
    #         'data': request.data,
    #     }
    #     return JsonResponse(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def userDetail(request, username, format=None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist or User.MultipleObjectsReturned:
        user = None

    if request.method == 'GET':
        if user is not None:
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        else:
            content = {
                'status': status.HTTP_404_NOT_FOUND,
                'data': {
                    'username': username,
                },
            }
            return JsonResponse(content, safe=False, status=status.HTTP_404_NOT_FOUND)


def badRequest(request, path):
    content = {
        'status': status.HTTP_400_BAD_REQUEST,
        'data': {
            'url': path,
        }
    }
    return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
