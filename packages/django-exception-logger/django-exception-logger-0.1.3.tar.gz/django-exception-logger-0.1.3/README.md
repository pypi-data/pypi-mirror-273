# django-exception_logger

# installation

## exception logger

- Add `exception_logger.middlewares.ExceptionLoggerMiddleware` to the beginning of the MIDDLEWARE list

```
MIDDLEWARE = [
    "exception_logger.middlewares.ExceptionLoggerMiddleware",
    # Django middlewares
]
```

- Register admin models
```
from exception_logger.admin import ExceptionModelAdmin, NoLogExceptionAdmin
from exception_logger.models import ExceptionModel, NoLogException

admin.site.register(ExceptionModel, ExceptionModelAdmin)
admin.site.register(NoLogException, NoLogExceptionAdmin)
```
 

## celery exception logger
- Register admin models
```
from exception_logger.admin import CeleryExceptionModelAdmin, NoLogCeleryExceptionAdmin
from exception_logger.models import CeleryExceptionModel, NoLogCeleryException

admin.site.register(CeleryExceptionModel, CeleryExceptionModelAdmin)
admin.site.register(NoLogCeleryException, NoLogCeleryExceptionAdmin)
```

##  request time logger

- Add `exception_logger.middlewares.RequestTimeMiddleware` to the end of the MIDDLEWARE list

```
MIDDLEWARE = [
    # Django middlewares
    "exception_logger.middlewares.RequestTimeMiddleware",
]
```

- Register admin model
```
from exception_logger.admin import RequestTimeAdmin
from exception_logger.models import RequestTime

admin.site.register(RequestTime, RequestTimeAdmin)
```
