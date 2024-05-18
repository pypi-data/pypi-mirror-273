from django.apps import AppConfig


class ExceptionLoggerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exception_logger"
    verbose_name = "Exception Logger"

    def ready(self):
        from . import signals
