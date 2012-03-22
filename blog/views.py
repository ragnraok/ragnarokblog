# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import list_detail, date_based
from ragnarokblog.blog.models import Article
from django.shortcuts import get_object_or_404, render_to_response
from tagging.models import Tag, TaggedItem
from django.conf import settings
import datetime
import logging

logger = logging.getLogger(__name__)

def archive_all_categories(request, **kwargs):
        logger.info('archive all categories')
        return list_detail.object_list(
                request,
                queryset=Article.objects.all(),
                template_object_name = 'category',
                **kwargs
                )

def article_list(request, page_size = 5, cur_page = 0, **kwargs):
        logger.info('archive all article')
        return list_detail.object_list(
                request,
                queryset=Article.objects.all().filter(status=Article.LIVE_STATUS).order_by('-publish_date'),
                paginate_by = page_size, # how many articles in each page
                page = cur_page, # the current page, default 0
                template_object_name = 'article',
                template_name= 'blog/article_list.html',
                **kwargs
                )

def archive_article_detail(request, year, month, day, slug, **kwargs):
        logger.info('archive an article, name ' + Article.objects.get(slug = slug).title)
        return date_based.object_detail(
                request,
                queryset = Article.objects.all(),
                year = year,
                month = month,
                day = day,
                slug = slug,
                date_field = 'publish_date',
                template_object_name = 'article',
                template_name= 'blog/article_detail.html',
                extra_context = {'site_url': settings.SITE_URL,
                                 'shortname': settings.DISQUS_WEBSITE_SHORTNAME}
                )

def tag_detail(request, slug, template_name = 'blog/tag_detail.html', **kwargs):
        tag = get_object_or_404(Tag, name__iexact = slug)
        logger.info('archive tag detail, name ' + str(tag))
        return list_detail.object_list(
                request,
                template_name = template_name,
                template_object_name = 'tag_article',
                queryset = TaggedItem.objects.get_by_model(Article, tag).filter(status=Article.LIVE_STATUS),
                extra_context = {'tag': tag},
                **kwargs
                )

def tag_list(request, template_name='blog/tag_list.html', **kwargs):
        logger.info('archive all tag')
        return list_detail.object_list(
                request,
                template_name = template_name,
                template_object_name = 'tag',
                queryset = Tag.objects.all(),
                **kwargs
                )

