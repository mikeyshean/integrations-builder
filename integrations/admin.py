from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from integrations.models import Category, Endpoint, Integration


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    list_display = ("id", "method", "path", "integration_link")

    def integration_link(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse(
                    "admin:integrations_integration_change", args=(obj.integration.pk,)
                ),
                obj.integration.name,
            )
        )

    integration_link.short_description = "integration"


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ("id", "integration_link", "category_link")
    readonly_fields = ("category_link",)

    def category_link(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:integrations_category_change", args=(obj.category.pk,)),
                obj.category.name,
            )
        )

    category_link.short_description = "category"

    def integration_link(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:integrations_integration_change", args=(obj.pk,)),
                obj.name,
            )
        )

    integration_link.short_description = "integration"
