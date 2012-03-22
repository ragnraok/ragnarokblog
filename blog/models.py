from django.db import models
from django.db.models import permalink, Manager
import logging
import datetime
from tagging.fields import TagField
from django.contrib.auth.models import User
import markdown

# Create your models here.

class Category(models.Model):
        """
        The blog article category
        """
        title = models.CharField(max_length=25, help_text="Maximum 250 letter")
        description = models.TextField(blank=True, help_text="Input your description here")
        slug = models.SlugField(unique=True)

        def __unicode__(self):
                return u'category ' + self.title

        def __str__(self):
                return u'category ' + self.title

        class Meta:
                db_table = 'blog_categories'
                ordering = ['title', ]
                verbose_name = 'atricles category'
                verbose_name_plural = 'articles categories'

        @permalink
        def get_absolute_url(self):
                return ('list_category_detail', (), {'slug': self.slug})

        def save(self):
                logger = logging.getLogger(__name__)
                logger.info("create a category, title " + self.title)

                super(Category, self).save()

class ArticleManager(Manager):
        def all_live(self):
                return self.get_query_set().all().filter(status=Article.LIVE_STATUS)

"""
    the Article is not use, because all data transfer into Articles_deamon
"""

class Article(models.Model):
        LIVE_STATUS = 1
        DRAFT_STATUS = 2
        STATUS_CHOICES = (
                (LIVE_STATUS, 'live'),
                (DRAFT_STATUS, 'draft'),
        )

        title = models.CharField(max_length=250, unique=True, help_text="maximum 250 letters")
        body = models.TextField(blank=False, editable=False)
        summary = models.TextField(blank=True, verbose_name="body")
        summary_html = models.TextField(editable=False, blank=True)
        publish_date = models.DateTimeField(default=datetime.datetime.now)
        status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
        enable_comment = models.BooleanField(default=True)
        author = models.ForeignKey(User, blank=False)
        tags = TagField(help_text="the tags for your article, separate by space")
        categories = models.ManyToManyField(Category, blank=True)
        slug = models.SlugField(unique_for_date="publish_date", blank=True, help_text='you have to input by yourself if the title is not English')

        objects = ArticleManager() 

        class Meta:
                verbose_name = "article"
                verbose_name_plural = "articles"
                db_table = "blog_articles"
                ordering = ['-publish_date', ]
                get_latest_by = 'publish_date'

        def __unicode__(self):
                return u"article: title " + self.title + ", writen by" + self.author.username
        
        def __str__(self):
                return u"article: title " + self.title + ", writen by" + self.author.username

        def save(self, *args, **kwargs):
                self.body = self.summary
                self.summary_html = markdown.markdown(self.summary, extensions=['codehilite'])

                self.body = markdown.markdown(self.body, extensions=['codehilite'])

                logger = logging.getLogger(__name__)
                logger.info("create an article, title " + self.title)

                super(Article, self).save(*args, **kwargs)
        
        @permalink
        def get_absolute_url(self):
                return ('article_detail', (), {'year': self.publish_date.year,
                                               'month': self.publish_date.strftime("%b").lower(),
                                               'day': self.publish_date.day,
                                               'slug': self.slug,
                                              })

class Articles_deamon(models.Model):
        """
           the blog article deamon, use for copy useage
        """
        LIVE_STATUS = 1
        DRAFT_STATUS = 2
        STATUS_CHOICES = (
                (LIVE_STATUS, 'live'),
                (DRAFT_STATUS, 'draft'),
        )

        title = models.CharField(max_length=250, help_text="maximum 250 letters")
        raw_markdown_body = models.TextField(blank=False)
        body = models.TextField(blank=False, editable=False)
        summary = models.TextField(help_text="a short summary of this article", blank=True)
        summary_html = models.TextField(editable=False, blank=True)
        publish_date = models.DateTimeField(default=datetime.datetime.now)
        status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
        enable_comment = models.BooleanField(default=True)
        author = models.ForeignKey(User, blank=False)
        tags = TagField(help_text="the tags for your article, separate by space")
        slug = models.SlugField(unique_for_date="publish_date", blank=True, help_text='you have to input by yourself if the title is not English')

        class Meta:
                verbose_name = "article"
                verbose_name_plural = "articles"
                db_table = "blog_articles_deamon"
                ordering = ['-publish_date', ]
                get_latest_by = 'publish_date'

        def __unicode__(self):
                return u"article: title " + self.title + ", writen by" + self.author.username
        
        def __str__(self):
                return u"article: title " + self.title + ", writen by" + self.author.username

        @permalink
        def get_absolute_url(self):
                return ('article_detail', (), {'year': self.publish_date.year,
                                               'month': self.publish_date.strftime("%b").lower(),
                                               'day': self.publish_date.day,
                                               'slug': self.slug,
                                              })

        def save(self, if_copy=False, *args, **kwargs):
                if self.summary:
                        self.summary_html = markdown.markdown(self.summary, extensions=['codehilite'])
                else:
                        if len(self.raw_markdown_body) > 2000:
                                self.summary = self.raw_markdown_body[:2000]
                        else:
                                self.summary = self.raw_markdown_body
                        self.summary_html = markdown.markdown(self.summary, extensions=['codehilite'])

                self.body = markdown.markdown(self.raw_markdown_body, extensions=['codehilite'])

                logger = logging.getLogger(__name__)
                logger.info("create an article_deamon, title " + self.title)

                if not if_copy:
                         try:
                                 a = Article.objects.get(title=self.title, body=self.raw_markdown_body, 
                                                         summary=self.summary, publish_date = self.publish_date,
                                                         status=self.status, enable_comment=self.enable_comment,
                                                         author=self.author, tags=self.tags, slug=self.slug)
                         except:
                                 Article.objects.create(title=self.title, body=self.raw_markdown_body, 
                                                        summary=self.summary, publish_date = self.publish_date,
                                                        status=self.status, enable_comment=self.enable_comment,
                                                        author=self.author, tags=self.tags, slug=self.slug)
 
                super(Articles_deamon, self).save(*args, **kwargs)

        

def copy_article():
    old_article_list = Article.objects.all()
    
    for article in old_article_list:
            temp = Articles_deamon(title=article.title, body=article.body, raw_markdown_body=article.body, 
                                   summary=article.summary, publish_date=article.publish_date, status=article.status, 
                                           enable_comment=article.enable_comment, author=article.author,
                                          tags=article.tags, slug=article.slug)
            temp.save(if_copy=True)
            
                



