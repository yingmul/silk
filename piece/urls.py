from django.conf.urls import patterns
from django.conf.urls import url
from piece.views import PieceDetailView, PieceCommentView

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)$', PieceDetailView.as_view(), name='piece-detail'),
    url(r'^comment/(?P<pk>\d+)/$', PieceCommentView.as_view(), name='piece-comment'),
)
