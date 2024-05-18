import json
from traceback import format_exc

from django.core.exceptions import RequestDataTooBig
from django.utils.deprecation import MiddlewareMixin

from exception_logger.models import ExceptionModel, NoLogException


class ExceptionLoggerMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            data = {}
        except RequestDataTooBig:
            data = "RequestDataTooBig"

        request._data_to_log = data

    def process_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        if NoLogException.objects.filter(exception=type(exception).__name__).exists():
            return

        ExceptionModel.objects.save_exception(
            method=request.method,
            path=request.path,
            data=request._data_to_log,
            query_params=request.GET,
            exception=repr(exception),
            traceback=format_exc(),
            headers=dict(request.headers),
            cookies=request.COOKIES,
            base_url=request.build_absolute_uri("/")[:-1],
        )
