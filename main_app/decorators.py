from functools import wraps

from django.utils.datetime_safe import datetime

from main_app.models import PageHit


def counted(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        page_hit = PageHit.objects.filter(url=request.request.path)
        if page_hit.count():
            page_count = page_hit.first().count
            page_hit.update(count=page_count+1, updated=datetime.now())
        else:
            page_hit.create(url=request.request.path)
        return func(request, *args, **kwargs)
    return wrapper
