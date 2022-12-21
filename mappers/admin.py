from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from mappers.models import Field, Model


class FieldInline(admin.TabularInline):
    model = Field
    fk_name = "model"
    exclude = ("created", "modified")
    # can_delete = False
    # verbose_name = 'Field'
    # verbose_name_plural = 'Fields'
    # extra = 0


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "target_model_links",
        "get_field_names",
        "is_remote",
    )
    list_display_links = ("id", "name", "target_model_links")
    inlines = (FieldInline,)
    exclude = ("created", "modified")

    def get_field_names(self, model):
        if model.fields.all():
            return [field.name for field in model.fields.all()]

    get_field_names.short_description = "fields"

    def target_model_links(self, model):
        if model.target_model:
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        "admin:mappers_model_change", args=(model.target_model_id,)
                    ),
                    model.target_model.name,
                )
            )

    target_model_links.short_description = "target_model"
