from __future__ import unicode_literals
from django.db import models


class Item(models.Model):
    link = models.URLField(max_length=255)
    time_published = models.DateTimeField()
    title = models.TextField()
    summary = models.TextField(default='')
    value = models.TextField()
