from django.db import models
from core.models import TimestampedModel


class Category(TimestampedModel):
    name = models.CharField(max_length=32, help_text="Name of the category")


class Integration(TimestampedModel):
    name = models.CharField(max_length=64, help_text="Name of the integration")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=False, blank=False)
