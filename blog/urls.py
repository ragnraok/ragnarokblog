from django.conf.urls.defaults import patterns, url
from ragnarokblog.blog.models import Category, Article

urlpatterns = patterns('ragnarokblog.blog.views',
    url(r'^$',
       view = "article_list",
       name =  "article_list"
    ),

    url(r'^tags/$',
       view = 'tag_list',
       name = 'blog_tag_list'),

    url(r'^tags/(?P<slug>[-\w]+)/$',
       view = 'tag_detail',
       name = 'blog_tag_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
       view = "archive_article_detail",
       name = 'article_detail'
    ),

    url(r'^(?P<page>\d+)/$',
       view = "article_list",
       name = "article_list_paginated"),

)
