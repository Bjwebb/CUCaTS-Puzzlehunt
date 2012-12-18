from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^add/(\d*)/(.*)$', 'track.views.add'),
)
