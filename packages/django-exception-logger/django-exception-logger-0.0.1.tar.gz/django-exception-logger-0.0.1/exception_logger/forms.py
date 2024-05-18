from django.forms import BaseInlineFormSet


class LimitModelFormset(BaseInlineFormSet):
    LIMIT = 20

    def __init__(self, *args, **kwargs):
        super(LimitModelFormset, self).__init__(*args, **kwargs)
        _kwargs = {self.fk.name: kwargs["instance"]}
        self.queryset = (
            kwargs["queryset"].filter(**_kwargs).order_by("-id")[: self.LIMIT]
        )
