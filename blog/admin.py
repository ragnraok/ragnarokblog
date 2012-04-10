from ragnarokblog.blog.models import Category, Article
from tagging.models import Tag
from django.contrib import admin
from django.conf import settings
from django.db import models
from django_markdown.widgets import MarkdownWidget
import os


class CategoryAdmin(admin.ModelAdmin):
        prepopulated_fields = {"slug": ("title", )} 
        list_display = ('title', 'slug', )

        class Media:
                pass

admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
        prepopulated_fields = {"slug": ("title", )}
        date_hierarchy = "publish_date"
        list_display = ('title', 'status', 'author', 'publish_date',)
        ordering = ['-publish_date']
        radio_fields = {'status': admin.HORIZONTAL}
        list_filter = ('enable_comment', 'status', )
        list_per_page = 30
        save_on_top = True

        formfield_overrides = {
                models.TextField: {'widget': MarkdownWidget},
        }

        fieldsets = (
                ('Basic', {
                        'classes': ('collapse', ),
                        'fields': ('title', 'author', 'slug', 'tags')
                }),
                ('Body', {
                        'fields': ('raw_body', ),
                }),
                ('Advanced', {
                        'classes': ('collapse', ),
                        'fields': ('status', 'enable_comment')
                })
        )

        class Media:
                js = [settings.STATIC_ROOT+'tiny_mce/tiny_mce.js',
                     os.path.join(settings.HERE, 'grappelli/static/grappelli/tinymce_setup.js')]

admin.site.register(Article, ArticleAdmin)

