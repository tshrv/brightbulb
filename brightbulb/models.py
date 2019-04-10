from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save


class Note(models.Model):
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(max_length=1000, null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=50, null=True)

    def __str__(self):
        return self.title

