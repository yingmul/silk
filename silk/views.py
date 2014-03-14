from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from sell.models import Picture


class LoginRequired(object):
    """
    Mixin for requiring login to a generic view.

    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs)


class HomeView(ListView):
    model = Picture
    template_name = 'silk/home.html'

    def get_queryset(self):
        return Picture.objects.filter(
            type='o',
            outfit__isnull=False,
            is_primary=True
        ).order_by('-outfit__created')
