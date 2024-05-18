from django.db.models import (
    Model,
    Manager,
    TextChoices,
    CharField,
    DateTimeField,
    TextField,
    JSONField,
    PositiveIntegerField,
    ForeignKey,
    CASCADE,
    UniqueConstraint,
)

from .enums import Method


class ExceptionManager(Manager):
    @staticmethod
    def save_exception(
        *,
        method,
        path,
        exception,
        traceback,
        data,
        query_params,
        headers,
        cookies,
        base_url,
    ):
        unique_data = {"method": method, "path": path, "exception": exception}

        exception_model = ExceptionModel.objects.filter(**unique_data).first()
        if exception_model is None:
            exception_model = ExceptionModel(**unique_data)

        exception_model.traceback = traceback
        exception_model.save()

        ExceptionDataModel.objects.create(
            exception=exception_model,
            data=data,
            query_params=query_params,
            headers=headers,
            cookies=cookies,
            base_url=base_url,
        )


class ExceptionModel(Model):
    method = CharField("Request method", max_length=8, choices=Method.choices)
    path = CharField("Request path", max_length=512)

    exception = TextField()
    traceback = TextField()

    count = PositiveIntegerField("Quantity", default=1)
    last_throw = DateTimeField("Last throw", auto_now=True)
    first_throw = DateTimeField("Fast throw", auto_now_add=True)

    objects = ExceptionManager()

    class Meta:
        verbose_name = "Exception"
        verbose_name_plural = "Exceptions"
        constraints = (
            UniqueConstraint(
                fields=("method", "path", "exception"), name="exception_path"
            ),
        )

    def __str__(self):
        return ""

    @property
    def short_exception(self):
        max_length = 30
        if len(self.exception) <= max_length:
            return self.exception

        return f"{self.exception[:max_length-3]}..."


class ExceptionDataModel(Model):
    exception = ForeignKey(ExceptionModel, on_delete=CASCADE)

    base_url = CharField(max_length=128)
    data = JSONField("Body", default=dict)
    query_params = JSONField("Query params", default=dict)
    headers = JSONField("Headers", default=dict)
    cookies = JSONField("Cookies", default=dict)

    datetime = DateTimeField("Date", auto_now_add=True)

    class Meta:
        verbose_name = "Throw data"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.pk or "-")


class NoLogException(Model):
    exception = CharField(max_length=256)

    class Meta:
        verbose_name = "No log Exception"
        verbose_name_plural = "No log Exceptions"

    def __str__(self):
        return self.exception
