from django.contrib import admin

from exception_logger.forms import LimitModelFormset
from exception_logger.models import ExceptionDataModel
from exception_logger.utils import pretty_json


class ExceptionDataModelInline(admin.StackedInline):
    formset = LimitModelFormset
    model = ExceptionDataModel
    fields = ("base_url", "data_", "query_params_", "headers_", "cookies_", "datetime")
    readonly_fields = fields
    extra = 0
    ordering = ("-datetime",)

    @admin.display(description="Body")
    def data_(self, obj):
        return pretty_json(obj.data)

    @admin.display(description="Query params")
    def query_params_(self, obj):
        return pretty_json(obj.query_params)

    @admin.display(description="Headers")
    def headers_(self, obj):
        return pretty_json(obj.headers)

    @admin.display(description="Cookies")
    def cookies_(self, obj):
        return pretty_json(obj.cookies)


class ExceptionModelAdmin(admin.ModelAdmin):
    inlines = (ExceptionDataModelInline,)
    fields = (
        "method",
        "path",
        "exception",
        "traceback",
        "count",
        "last_throw",
        "first_throw",
    )
    readonly_fields = fields
    list_display = (
        "method",
        "path",
        "short_exception",
        "count",
        "last_throw",
        "first_throw",
    )
    ordering = ("-count", "-last_throw")
    list_display_links = ("method", "path", "short_exception")
    list_filter = ("method",)
    search_fields = ("path", "method", "exception")

    @admin.display(description="exception")
    def short_exception(self, obj):
        return obj.short_exception

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class NoLogExceptionAdmin(admin.ModelAdmin):
    list_display = ("exception",)
    list_display_links = ("exception",)
    search_fields = ("exception",)

    def has_change_permission(self, request, obj=None):
        return False
