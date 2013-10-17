from django.conf.urls import patterns
from django.conf.urls import url
from sell.views import SellOutfitView

urlpatterns = patterns('',
    url(r'^$', SellOutfitView.as_view(), name='sell-outfit'),
)
