from django.conf.urls import patterns
from django.conf.urls import url
from django.conf import settings
from sell.views import SellWizard, \
    PictureCreateView, PictureDeleteView, PictureListView, PictureMakePrimaryView
from sell.forms import SellOutfitForm, SellPieceForm, SellPreviewForm

# allow maximum of 10 sell piece forms, HACK
sell_forms = [SellOutfitForm]
for i in range(settings.MAX_PIECE_SELL_FORMS):
    sell_forms.append(SellPieceForm)
sell_forms.append(SellPreviewForm)

urlpatterns = patterns('',
    url(r'^$', SellWizard.as_view(sell_forms)),
    # urls for creating pictures for outfit
    url(r'^new/$', PictureCreateView.as_view(), name='sell-new'),
    url(r'^view/$', PictureListView.as_view(), name='sell-view'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='sell-delete'),
    url(r'^makePrimary/(?P<step>\d+)/(?P<pk>\d+)$', PictureMakePrimaryView.as_view(), name='sell-make-primary'),

    # urls for creating pictures for piece
    url(r'^piece/new/(?P<step>\d+)/$', PictureCreateView.as_view(), {'piece':True}, name='sell-piece-new'),
    url(r'^piece/view/(?P<step>\d+)/$', PictureListView.as_view(), {'piece':True}, name='sell-piece-view'),
    url(r'^piece/makePrimary/(?P<step>\d+)/(?P<pk>\d+)/$', PictureMakePrimaryView.as_view(), {'piece':True}, name='sell-piece-make-primary'),
)
