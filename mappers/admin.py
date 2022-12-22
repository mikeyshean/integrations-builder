from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from mappers.models import Field, FieldMap, Map, Model, ModelMap, Transformer


class FieldInline(admin.TabularInline):
    model = Field
    fk_name = "model"
    exclude = ("created", "modified")


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "get_field_names",
    )
    list_display_links = ("id", "name")
    inlines = (FieldInline,)
    exclude = ("created", "modified")

    def get_field_names(self, model):
        if model.fields.all():
            return [field.name for field in model.fields.all()]

    get_field_names.short_description = "fields"


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "type",
        "choices",
        "list_item_type",
        "object_model_link",
    )
    list_display_links = (
        "id",
        "name",
        "object_model_link",
    )
    exclude = ("created", "modified")

    def object_model_link(self, model):
        if model.object_model:
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        "admin:mappers_model_change", args=(model.object_model_id,)
                    ),
                    model.object_model.name,
                )
            )

    object_model_link.short_description = "object model"


@admin.register(Transformer)
class TransformerAdmin(admin.ModelAdmin):

    list_display = ("type",)
    list_display_links = ("type",)
    exclude = ("created", "modified")


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):

    list_display = ("id", "source_model", "target_model")
    list_display_links = ("id",)
    exclude = ("created", "modified")


@admin.register(ModelMap)
class TargetModelAdmin(admin.ModelAdmin):

    list_display = ("id", "map", "source_model", "target_model")
    list_display_links = ("id", "map")
    exclude = ("created", "modified")


@admin.register(FieldMap)
class TargetFieldAdmin(admin.ModelAdmin):

    list_display = ("id", "map", "source_field", "target_field", "transformer")
    list_display_links = ("id", "map")
    exclude = ("created", "modified")
