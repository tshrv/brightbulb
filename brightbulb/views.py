# DJANGO
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# REST_FRAMEWORK
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# MODELS
from django.contrib.auth.models import User
from .models import Note
# SERIALIZERS
from .serializers import UserSerializer, NoteSerializer
# AUTH
from .auth import BearerAuthentication
# PERMISSIONS
# from .permissions import
# UTILS
from .utils import gen_response, uniquely_slugify


# USERS
@api_view(['GET'])
@authentication_classes((BearerAuthentication,))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def user_list(request, format=None):
    if request.method == 'GET':
        serializer = UserSerializer(User.objects.all(), many=True)
        return gen_response(status.HTTP_200_OK, serializer.data,)


@api_view(['POST'])
@csrf_exempt
def user_register(request, format=None):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # vulnerable: raw password being saved initially
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return gen_response(status.HTTP_201_CREATED, serializer.data,)
        else:
            return gen_response(status.HTTP_406_NOT_ACCEPTABLE, request.data, serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((BearerAuthentication,))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def user_detail(request, username, format=None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist or User.MultipleObjectsReturned:
        user = None

    if request.method == 'GET':
        if user is not None:
            serializer = UserSerializer(user)
            return gen_response(status.HTTP_200_OK, serializer.data)
        else:
            return gen_response(status.HTTP_404_NOT_FOUND, {'username':username})

    elif request.method == 'PUT':
        if request.user is not user:
            return gen_response(status.HTTP_401_UNAUTHORIZED, request.data)

        if user is not None:
            # flow error: requires all data of the user
            serializer = UserSerializer(instance=user, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(user.password)
                user.save()
                return gen_response(status.HTTP_202_ACCEPTED, serializer.data)
            else:
                return gen_response(status.HTTP_406_NOT_ACCEPTABLE, request.data, serializer.errors)
        else:
            gen_response(status.HTTP_404_NOT_FOUND, request.data)

    elif request.method == 'DELETE':
        if user is not None:
            # flow error: requires all data of the user
            user.delete()
            return gen_response(status.HTTP_200_OK, {'username': username})
        else:
            return gen_response(status.HTTP_404_NOT_FOUND, {'username': username})


# NOTES
@api_view(['GET', 'POST'])
@authentication_classes((BearerAuthentication,))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def note_list_create(request):
    if request.method == 'GET':
        serializer = NoteSerializer(Note.objects.filter(owner=request.user), many=True)
        return gen_response(status.HTTP_200_OK, serializer.data)
    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            note = serializer.save()
            note.owner = request.user
            note.slug = uniquely_slugify(note.title, Note)
            note.save()
            return gen_response(status.HTTP_201_CREATED, NoteSerializer(note).data)
        else:
            return gen_response(status.HTTP_406_NOT_ACCEPTABLE, serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((BearerAuthentication,))
@permission_classes((IsAuthenticated,))
@csrf_exempt
def note_detail(request, slug, format=None):
    try:
        note = Note.objects.get(slug__iexact=slug, owner=request.user)
    except Note.DoesNotExist:
        return gen_response(status.HTTP_404_NOT_FOUND, {'slug': slug})

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return gen_response(status.HTTP_200_OK, serializer.data)

    elif request.method == 'PUT':
        serializer = NoteSerializer(data=request.data, instance=note)
        if serializer.is_valid():
            note = serializer.save()
            note.slug = uniquely_slugify(note.title)
            note.save()
            return gen_response(status.HTTP_202_ACCEPTED, NoteSerializer(note).data)
        else:
            return gen_response(status.HTTP_406_NOT_ACCEPTABLE, serializer.errors)

    elif request.method == 'DELETE':
        note.delete()
        return gen_response(status.HTTP_200_OK, {'slug': slug})


# BAD_REQUEST
def bad_request(request, path):
    content = {
        'status': status.HTTP_400_BAD_REQUEST,
        'data': {
            'url': path,
        }
    }
    return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)


# DESCRIPTION
def description(request):
    return render(request, 'brightbulb/description.html')
