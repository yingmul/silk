from django.conf.urls import patterns, include, url
from silkers.views import RegistrationWizard, LoginView
from silkers.forms import RegistrationBasicForm, RegistrationExtraForm
from silk.views import HomeView
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
    url(r'^register/$', RegistrationWizard.as_view([RegistrationBasicForm, RegistrationExtraForm]), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'silkers.views.logout_view', name='logout'),

    url(r'^sell/', include('sell.urls')),
    url(r'^outfit/', include('outfit.urls')),
    url(r'^piece/', include('piece.urls')),
)

#TODO: configure web server to serve static file via MEDIA_URL in settings
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))

