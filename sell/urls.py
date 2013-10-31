from django.conf.urls import patterns
from django.conf.urls import url
from django.conf import settings
from sell.views import SellWizard, \
    PictureCreateView, PictureDeleteView, PictureListView, show_more_piece_form_condition
from sell.forms import SellOutfitForm, SellPieceForm, SellPreviewForm

# allow maximum of 10 sell piece forms, HACK
sell_forms = [SellOutfitForm]
for i in range(settings.MAX_PIECE_SELL_FORMS):
    sell_forms.append(SellPieceForm)
sell_forms.append(SellPreviewForm)

# for step 2 to 10 of sell process, needs to know if it needs to skip as a step
cond_dict = {}
for i in range(2, settings.MAX_PIECE_SELL_FORMS+1):
    cond_dict[str(i)] = show_more_piece_form_condition

urlpatterns = patterns('',
    url(r'^$', SellWizard.as_view(sell_forms, condition_dict=cond_dict)),
    # urls for creating pictures for outfit
    url(r'^new/$', PictureCreateView.as_view(), name='sell-new'),
    url(r'^view/$', PictureListView.as_view(), name='sell-view'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='sell-delete'),

    # urls for creating pictures for piece
    url(r'^piece/new/$', PictureCreateView.as_view(), {'piece':True}, name='sell-piece-new'),
    url(r'^piece/view/$', PictureListView.as_view(), {'piece':True}, name='sell-piece-view'),
)
