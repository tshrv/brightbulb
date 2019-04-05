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


@api_view(['GET', 'POST'])
@csrf_exempt
def user_list(request, format=None):
    if request.method == 'GET':
        serializer = UserSerializer(User.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # vulnerable: raw password being saved initially
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            content = {
                'status': status.HTTP_201_CREATED,
                'data': serializer.data,
            }
            return JsonResponse(content, safe=False, status=status.HTTP_201_CREATED)
        else:
            content = {
                'status': status.HTTP_406_NOT_ACCEPTABLE,
                'data': request.data,
                'error': serializer.errors,
            }
            return JsonResponse(content, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)


def bad_request(request, path):
    content = {
        'status': status.HTTP_400_BAD_REQUEST,
        'data': {
            'url': path,
        }
    }
    return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def user_detail(request, username, format=None):
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

    elif request.method == 'PUT':
        if user is not None:
            # flow error: requires all data of the user
            serializer = UserSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(user.password)
                user.save()
                content = {
                    'status': status.HTTP_202_ACCEPTED,
                    'data': serializer.data,
                }
                return JsonResponse(content, safe=False, status=status.HTTP_202_ACCEPTED)
            else:
                content = {
                    'status': status.HTTP_406_NOT_ACCEPTABLE,
                    'data': request.data,
                    'error': serializer.errors,
                }
                return JsonResponse(content, safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            content = {
                'status': status.HTTP_404_NOT_FOUND,
                'data': request.data,
            }
            return JsonResponse(content, safe=False, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        if user is not None:
            # flow error: requires all data of the user
            user.delete()
            content = {
                'status': status.HTTP_200_OK,
                'data': {
                    'username': username,
                },
            }
            return JsonResponse(content, safe=False, status=status.HTTP_200_OK)
        else:
            content = {
                'status': status.HTTP_404_NOT_FOUND,
                'data': {
                    'username': username,
                },
            }
            return JsonResponse(content, safe=False, status=status.HTTP_404_NOT_FOUND)
