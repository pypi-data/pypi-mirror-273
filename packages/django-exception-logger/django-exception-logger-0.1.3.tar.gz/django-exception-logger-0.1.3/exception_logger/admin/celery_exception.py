from django.contrib import admin

from exception_logger.forms import LimitModelFormset
from exception_logger.models import CeleryExceptionDataModel
from exception_logger.utils import pretty_json


class CeleryExceptionDataModelInline(admin.StackedInline):
    formset = LimitModelFormset
    model = CeleryExceptionDataModel
    fields = ("_args", "_kwargs", "datetime")
    readonly_fields = fields
    extra = 0
    ordering = ("-datetime",)

    @admin.display(description="args")
    def _args(self, obj):
        return pretty_json(obj.data)

    @admin.display(description="kwargs")
    def _kwargs(self, obj):
        return pretty_json(obj.query_params)


class CeleryExceptionModelAdmin(admin.ModelAdmin):
    inlines = (CeleryExceptionDataModelInline,)
    fields = (
        "task",
        "exception",
        "traceback",
        "count",
        "last_throw",
        "first_throw",
    )
    readonly_fields = fields
    list_display = (
        "task",
        "short_exception",
        "count",
        "last_throw",
        "first_throw",
    )
    ordering = ("-count", "-last_throw")
    list_display_links = ("task", "short_exception")
    search_fields = ("task", "exception")

    @admin.display(description="exception")
    def short_exception(self, obj):
        return obj.short_exception

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class NoLogCeleryExceptionAdmin(admin.ModelAdmin):
    list_display = ("exception",)
    list_display_links = ("exception",)
    search_fields = ("exception",)

    def has_change_permission(self, request, obj=None):
        return False
