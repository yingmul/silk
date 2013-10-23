from django.conf.urls import patterns
from django.conf.urls import url
from sell.views import SellWizard, PictureCreateView, PictureDeleteView, PictureListView
from sell.forms import SellOutfitStepOneForm, SellOutfitStepTwoForm

urlpatterns = patterns('',
    # url(r'^$', SellOutfitView.as_view(), name='sell-outfit'),
    url(r'^$', SellWizard.as_view([SellOutfitStepOneForm, SellOutfitStepTwoForm])),
    url(r'^new/$', PictureCreateView.as_view(), name='sell-new'),
    url(r'^view/$', PictureListView.as_view(), name='sell-view'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='sell-delete'),
)
