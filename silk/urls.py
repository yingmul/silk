from django.conf.urls import patterns, include, url
from silkers.views import RegistrationWizard, LoginView
from silkers.forms import RegistrationBasicForm, RegistrationExtraForm
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^silk/', include('silk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'silk.views.home', name='home'),
    url(r'^register/$', RegistrationWizard.as_view([RegistrationBasicForm, RegistrationExtraForm])),
    url(r'^login/$', LoginView.as_view()),
    url(r'^sell/', include('sell.urls')),
)
