from django.conf.urls.defaults import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^accounts/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/puzzles/')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^q/', include('questionnaire.urls')),
    url(r'^track/', include('track.urls')),
    url('^', include('main.urls')),
    url('^', include('secret.urls')),
    url('^(.*/)$', 'django.contrib.flatpages.views.flatpage'),
)
