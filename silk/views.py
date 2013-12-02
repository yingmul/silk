from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from sell.models import Picture, Outfit, Piece

class LoginRequired(object):
    """
    Mixin for requiring login to a generic view.

    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequired, self).dispatch(*args, **kwargs)


class HomeView(LoginRequired, ListView):
    model = Picture
    template_name = 'silk/home.html'

    def get_queryset(self):
        return Picture.objects.filter(
            seller=self.request.user,
            type='o',
            outfit__isnull=False,
            is_primary=True
        )


class OutfitDetailView(LoginRequired, DetailView):
    model = Outfit
    template_name = 'silk/outfit_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OutfitDetailView, self).get_context_data(**kwargs)
        piece_pictures = []
        for piece in self.object.piece_set.all():
            for picture in piece.picture_set.all():
                if picture.is_primary:
                    piece_pictures.append(picture)
                    break

        context['piece_pictures'] = piece_pictures
        return context


class PieceDetailView(LoginRequired, DetailView):
    model = Piece
    template_name = 'silk/piece_detail.html'


