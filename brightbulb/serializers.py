from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('id', 'password')


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ('id', 'owner')
