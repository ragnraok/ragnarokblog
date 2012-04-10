from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.shortcuts import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ragnarokblog.views.home', name='home'),
    # url(r'^ragnarokblog/', include('ragnarokblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', lambda request: HttpResponseRedirect('/blog/')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^testlog/$', 'ragnarokblog.blog.views.test'),

    url(r'^blog/', include('ragnarokblog.blog.urls')),

    url(r'^feed/', include('ragnarokblog.feed.urls')),

    url(r'^about/$', 'ragnarokblog.views.render_about'),

    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^markdown/', include('django_markdown.urls')),

)

urlpatterns += patterns('',

         url(r'^tiny_mce(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.STATIC_ROOT + '/tiny_mce'}),

         url(r'^css/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.STATIC_ROOT + '/css'}),

         url(r'^static(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.STATIC_ROOT})
)
