import json
from django.views.generic import DetailView
from django.views.generic.edit import BaseFormView
from django.http import HttpResponse

from sell.models import Piece, Picture
from silk.views import LoginRequired
from piece.forms import CommentForm
from piece.models import Comment


class PieceDetailView(DetailView):
    model = Piece
    template_name = 'piece/piece_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PieceDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(
            piece=self.get_object().pk
        ).order_by('created')

        other_outfit_pictures = Picture.objects.filter(
            seller=self.get_object().outfit.user,
            is_primary=True,
            type='o',
            outfit__isnull=False,
        ).exclude(
            outfit=self.get_object().outfit
        ).order_by('-outfit__created')[:8]

        context.update({
            'comment_form': CommentForm(),
            'comments': comments,
            'other_outfits': other_outfit_pictures
        })

        return context


class PieceCommentView(LoginRequired, BaseFormView):
    form_class = CommentForm
    def form_valid(self, form):
        comment = form.cleaned_data['comment']
        author = self.request.user

        # create a new Comment object
        piece_pk = self.kwargs.get('pk')
        piece = Piece.objects.get(pk=piece_pk)
        Comment.objects.create(
            author=author,
            comment=comment,
            piece=piece,
        )

        num_comments = Comment.objects.filter(piece=piece).count()

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
