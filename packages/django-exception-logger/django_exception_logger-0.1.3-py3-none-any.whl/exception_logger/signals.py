from django.db.models.signals import post_save
from django.dispatch import receiver

from exception_logger.models import (
    ExceptionDataModel,
    NoLogException,
    ExceptionModel,
    NoLogCeleryException,
    CeleryExceptionModel,
)


@receiver(signal=post_save, sender=ExceptionDataModel)
def update_exception(sender, instance, **kwargs):
    exception_model = instance.exception
    exception_model.last_throw = instance.datetime
    exception_model.count = exception_model.exceptiondatamodel_set.count()
    exception_model.save()


@receiver(signal=post_save, sender=NoLogException)
def delete_exceptions(sender, instance, created, **kwargs):
    if not created:
        return

    ExceptionModel.objects.filter(exception__startswith=instance.exception).delete()


try:
    from celery.signals import task_retry, task_failure, task_revoked

    @task_retry.connect
    @task_failure.connect
    @task_revoked.connect
    def celery_on_failure(signal, sender, exception, einfo, **kwargs):
        if NoLogCeleryException.objects.filter(
            exception=type(exception).__name__
        ).exists():
            return

        CeleryExceptionModel.objects.save_exception(
            task=sender.name,
            exception=repr(exception),
            traceback=einfo.traceback,
            args=kwargs["args"],
            kwargs=kwargs["kwargs"],
        )

except ImportError:
    pass
