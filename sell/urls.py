from django.conf.urls import patterns
from django.conf.urls import url
from sell.views import SellOutfitView, PictureCreateView, PictureDeleteView, PictureListView

urlpatterns = patterns('',
    url(r'^$', SellOutfitView.as_view(), name='sell-outfit'),
    url(r'^new/$', PictureCreateView.as_view(), name='sell-new'),
    url(r'^view/$', PictureListView.as_view(), name='sell-view'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='sell-delete'),
)
