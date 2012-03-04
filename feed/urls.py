from django.conf.urls.defaults import patterns, url
from ragnarokblog.feed.views import AtomFeed

urlpatterns = patterns('',

    url(r'^$',
       view = AtomFeed()),
)

