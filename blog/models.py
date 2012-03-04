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

class Article(models.Model):
        """
           the blog article 
        """
        LIVE_STATUS = 1
        DRAFT_STATUS = 2
        STATUS_CHOICES = (
                (LIVE_STATUS, 'live'),
                (DRAFT_STATUS, 'draft'),
        )

        title = models.CharField(max_length=250, help_text="maximum 250 letters")
        body = models.TextField(blank=False)
        summary = models.TextField(help_text="a short summary of this article", blank=True)
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

        def save(self):
                if self.summary:
                        self.summary_html = self.summary
                else:
                        if len(self.body) > 150:
                                self.summary = self.body[:150]
                        else:
                                self.summary = self.body
                        self.summary_html = markdown.markdown(self.summary, output_format="html")

                logger = logging.getLogger(__name__)
                logger.info("create an article, title " + self.title)

                super(Article, self).save()
        
        @permalink
        def get_absolute_url(self):
                return ('article_detail', (), {'year': self.publish_date.year,
                                               'month': self.publish_date.strftime("%b").lower(),
                                               'day': self.publish_date.day,
                                               'slug': self.slug,
                                              })
        

                      
                



