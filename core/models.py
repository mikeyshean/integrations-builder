from django.db import models
from django.utils import timezone

class TimestampedModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True