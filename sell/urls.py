from django.conf.urls import patterns
from django.conf.urls import url
from sell.views import SellWizard, PictureCreateView, PictureDeleteView, PictureListView
from sell.forms import SellOutfitStepOneForm, SellOutfitStepTwoForm

urlpatterns = patterns('',
    url(r'^$', SellWizard.as_view([SellOutfitStepOneForm, SellOutfitStepTwoForm])),
    # urls for creating pictures for outfit
    url(r'^new/$', PictureCreateView.as_view(), name='sell-new'),
    url(r'^view/$', PictureListView.as_view(), name='sell-view'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='sell-delete'),

    # urls for creating pictures for piece
    url(r'^piece/new/$', PictureCreateView.as_view(), {'piece':True}, name='sell-piece-new'),
    url(r'^piece/view/$', PictureListView.as_view(), {'piece':True}, name='sell-piece-view'),
)
