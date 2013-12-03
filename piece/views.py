from django.views.generic import DetailView
from sell.models import Piece
from silk.views import LoginRequired


class PieceDetailView(LoginRequired, DetailView):
    model = Piece
    template_name = 'piece/piece_detail.html'
