from django.contrib import admin


class RequestTimeAdmin(admin.ModelAdmin):
    fields = ("method", "path", "average_with_delta_error", "quantity")
    list_display = ("method", "path", "average_with_delta_error", "quantity")
    list_display_links = ("method", "path")
    list_filter = ("method",)
    search_fields = ("path", "method")
    ordering = ("-average_time", "-quantity")

    @admin.display(description="Время запроса, сек")
    def average_with_delta_error(self, obj):
        return f"{round(obj.average_time, 6)} ± {round(obj.error_delta, 6)}"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
