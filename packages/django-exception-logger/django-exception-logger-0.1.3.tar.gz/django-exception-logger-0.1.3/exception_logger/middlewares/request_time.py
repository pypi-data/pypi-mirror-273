from time import time

from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

from exception_logger.models import RequestTime


class RequestTimeMiddleware(MiddlewareMixin):
    start_time = None

    def process_request(self, request):
        self.start_time = time()

    def process_response(self, request, response):
        time_delta = time() - self.start_time
        RequestTime.objects.update_request_time(
            method=request.method,
            path=resolve(request.path).route,
            time_delta=time_delta,
        )
        return response
