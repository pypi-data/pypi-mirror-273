from django.core.exceptions import ObjectDoesNotExist
from django.db.models import (
    Model,
    FloatField,
    CharField,
    Manager,
    PositiveIntegerField,
    UniqueConstraint,
)

from .enums import Method


class RequestTimeManager(Manager):
    def update_request_time(self, *, method, path, time_delta):
        try:
            request_time = self.get(method=method, path=path)
        except ObjectDoesNotExist:
            request_time = self.model(method=method, path=path)

        request_time.quantity += 1

        n = request_time.quantity  # quantity
        x_n = time_delta  # last value

        request_time.average_time = (request_time.average_time * (n - 1) + x_n) / n

        if n > 1:
            request_time.dispersion = (request_time.dispersion * (n - 2) / n) + (
                x_n**2 / (n * (n - 1))
            )

        request_time.save()


class RequestTime(Model):
    Method = Method

    method = CharField("Request method", max_length=8, choices=Method.choices)
    path = CharField("Request path", max_length=512)

    average_time = FloatField("Average request time", default=0)
    dispersion = FloatField("Dispersion", default=0)
    quantity = PositiveIntegerField("Quantity", default=0)

    objects = RequestTimeManager()

    class Meta:
        verbose_name = "Request time"
        verbose_name_plural = "Request times"
        constraints = (
            UniqueConstraint(fields=("method", "path"), name="request_path"),
        )

    def __str__(self):
        return ""

    @property
    def error_delta(self):  # погрешность
        return self.dispersion ** (1 / 2)
