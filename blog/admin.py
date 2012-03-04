from ragnarokblog.blog.models import Category, Article
from tagging.models import Tag
from django.contrib import admin
from django.conf import settings
from django.db import models
from ragnarokblog.filebrowser.widgets import FileInput
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
        raw_id_fields = ('categories', )
        list_filter = ('enable_comment', 'status', )
        list_per_page = 30
        save_on_top = True

        formfield_overrides = {
                models.ImageField:{'widget': FileInput}
        }

        fieldsets = (
                (None, {
                        'fields': ('title', 'body', 'author', 'slug', 'tags')
                }),
                ('Advanced', {
                        'classes': ('collapse', ),
                        'fields': ('summary', 'status', 'enable_comment', 'categories')
                })
        )

        class Media:
                js = [settings.STATIC_ROOT+'tiny_mce/tiny_mce.js',
                     os.path.join(settings.HERE, 'grappelli/static/grappelli/tinymce_setup.js')]

admin.site.register(Article, ArticleAdmin)

