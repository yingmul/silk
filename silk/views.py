import simplejson
from functools import wraps
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from sell.models import Picture


def ajax_login_required(function=None,redirect_field_name=None):
    """
    Returns Http status code 401 if user is not authenticated
    """
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            print 'ajax login decorator request', request
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(status=401)
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)


class LoginRequired(object):
    """
    Mixin for requiring login to a generic view.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs)


class AjaxLoginRequired(object):
    """
    Mixin for requiring login to a view that pops up a login modal
    """
    @method_decorator(ajax_login_required)
    def dispatch(self, *args, **kwargs):
        return super(AjaxLoginRequired, self).dispatch(*args, **kwargs)


class HomeView(ListView):
    model = Picture
    template_name = 'silk/home.html'

    def get_queryset(self):
        return Picture.objects.filter(
            type='o',
            outfit__isnull=False,
            is_primary=True
        ).order_by('-outfit__created')
