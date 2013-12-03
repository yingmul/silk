from django.views.generic import DetailView
from django.http import HttpResponse
from sell.models import Outfit
from silk.views import LoginRequired

def like_outfit(request, pk):
    outfit = Outfit.objects.get(pk=pk)
    outfit.num_likes += 1
    outfit.save()
    return HttpResponse(outfit.num_likes)


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

        context['piece_pictures'] = piece_pictures
        return context
