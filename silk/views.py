from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def home(request):
    return HttpResponse("Welcome to SILK!")


class LoginRequired(object):
    """
    Mixin for requiring login to a generic view.

    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs)

