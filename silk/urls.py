from django.conf.urls import patterns, include, url
from silk.views import HomeView
from silkers.views import ProfileView
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^silk/', include('silk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^register/$', 'silkers.views.ajax_registration', name='register'),
    # url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login/$', 'silkers.views.ajax_login', name='login'),
    url(r'^logout/$', 'silkers.views.logout_view', name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),

    url(r'^feedback/$', 'silkers.views.feedback', name='feedback'),
    url(r'^sell/', include('sell.urls')),
    url(r'^outfit/', include('outfit.urls')),
    url(r'^piece/', include('piece.urls')),
)

#TODO: configure web server to serve static file via MEDIA_URL in settings
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))

