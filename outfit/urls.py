from django.conf.urls import patterns
from django.conf.urls import url
from outfit.views import OutfitDetailView, like_outfit

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)$', OutfitDetailView.as_view(), name='outfit-detail'),
    url(r'^like/(?P<pk>\d+)$', like_outfit, name='outfit-like'),
)
