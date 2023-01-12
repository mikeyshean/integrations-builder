from django.db import models

from core.models import TimestampedModel


class Category(TimestampedModel):
    name = models.CharField(
        max_length=32, help_text="Name of the category", unique=True
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Integration(TimestampedModel):
    name = models.CharField(max_length=64, help_text="Name of the integration")
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=False, blank=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"], name="unique_name_and_category"
            )
        ]

    def __str__(self) -> str:
        return self.name


class Domain(TimestampedModel):
    domain = models.CharField(max_length=64, help_text="Base domain of API")
    integration = models.ForeignKey(
        "Integration",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="domains",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["integration", "domain"], name="unique_integration_and_domain"
            )
        ]

    def __str__(self) -> str:
        return self.domain


class Endpoint(TimestampedModel):
    method = models.CharField(max_length=8, help_text="HTTP Method")
    path = models.CharField(max_length=64, help_text="API endpoint path")
    integration = models.ForeignKey(
        "Integration",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="endpoints",
    )
    model = models.ForeignKey(
        "mappers.Model", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["integration", "path", "method"],
                name="unique_integration_path_method",
            )
        ]

    def __str__(self) -> str:
        return f"{self.method} - {self.path}"
