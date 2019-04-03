from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(max_length=1000, null=False)

    def __str__(self):
        return self.title
