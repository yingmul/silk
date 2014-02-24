from django.conf.urls import patterns
from django.conf.urls import url
from outfit.views import OutfitDetailView, OutfitCommentView, like_outfit, get_outfit_pictures

urlpatterns = patterns('',
    url(r'^detail/(?P<pk>\d+)$', OutfitDetailView.as_view(), name='outfit-detail'),
    url(r'^like/(?P<pk>\d+)/(?P<like>\w+)/$', like_outfit, name='outfit-like'),
    url(r'^pictures/(?P<pk>\d+)$', get_outfit_pictures, name="outfit-get-pictures"),
    url(r'^comment/(?P<pk>\d+)/$', OutfitCommentView.as_view(), name='outfit-comment'),
)
