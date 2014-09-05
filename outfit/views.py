import simplejson as json
from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import BaseFormView
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from sell.models import Outfit, Picture
from silk.views import AjaxLoginRequired
from piece.forms import CommentForm
from piece.models import Comment

def like_outfit(request, pk, like):
    outfit = Outfit.objects.get(pk=pk)
    if like == 'true':
        outfit.num_likes += 1
    else:
        outfit.num_likes -= 1
    outfit.save()
    return HttpResponse(outfit.num_likes)

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


class OutfitDetailView(DetailView):
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

        comments = Comment.objects.filter(
            outfit=self.get_object().pk
        ).order_by('created')

        context.update({
            'piece_pictures': piece_pictures,
            'comment_form': CommentForm(),
            'comments': comments,
        })

        return context

#TODO: perhaps move this to MyAccount page's posted outfit page, then have it redirect
#to the MyAccount page instead of home page
class OutfitDeleteView(DeleteView):
    model = Outfit
    success_url = settings.LOGIN_REDIRECT_URL

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(OutfitDeleteView, self).get_object()
        return obj

    # only allow delete when logged in
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        resp = super(OutfitDeleteView, self).dispatch(*args, **kwargs)
        return resp


class OutfitCommentView(AjaxLoginRequired, BaseFormView):
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.cleaned_data['comment']
        author = self.request.user

        # create a new Comment object
        outfit_pk = self.kwargs.get('pk')
        outfit = Outfit.objects.get(pk=outfit_pk)
        Comment.objects.create(
            author=author,
            comment=comment,
            outfit=outfit,
        )

        num_comments = Comment.objects.filter(outfit=outfit).count()

        result = {
            'comment': comment,
            'author': author.username,
            'num_comments': num_comments,
        }

        return HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status=200
        )
