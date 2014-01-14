import simplejson as json
from django.views.generic import DetailView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from sell.models import Outfit, Piece, Picture
from silk.views import LoginRequired

@login_required
def like_outfit(request, pk):
    outfit = Outfit.objects.get(pk=pk)
    outfit.num_likes += 1
    outfit.save()
    return HttpResponse(outfit.num_likes)

@login_required
def get_outfit_pictures(request, pk):
    """
    Given a pk for an outfit, return all the outfit pictures except for the primary photo
    This is for the home page when user hovers over an outfit.
    """
    outfit_urls = []
    outfit = Outfit.objects.get(pk=pk)
    pictures = Picture.objects.filter(
        outfit=outfit,
        is_primary=False,
    )
    for pic in pictures:
        outfit_urls.append(pic.thumbnail_url)

    return HttpResponse(json.dumps(outfit_urls), mimetype=u'application/json')


class OutfitDetailView(LoginRequired, DetailView):
    model = Outfit
    template_name = 'outfit/outfit_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OutfitDetailView, self).get_context_data(**kwargs)
        piece_pictures = []

        for piece in self.object.piece_set.all():
            for picture in piece.picture_set.all():
                if picture.is_primary:
                    piece_pictures.append(picture)
                    break

        context.update({
            'piece_pictures': piece_pictures
        })

        return context
