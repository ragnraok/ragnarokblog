# Create your views here.
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from ragnarokblog.blog.models import Article

class LastestArticlesFeed(Feed):
        title = "Ragnarok"
        link = "/feed/"
        description = "Updates on changes and addition to ragnarok blog"
        feed_type = Rss201rev2Feed

        def items(self):
                return Article.objects.order_by('-publish_date')[:20]

        def item_title(self, item):
                return item.title

        def item_description(self, item):
                return item.summary_html

        def item_link(self, item):
                return item.get_absolute_url()

        def item_pubdate(self, item):
                return item.publish_date


class AtomFeed(LastestArticlesFeed):
        feed_type = Atom1Feed
        subtitle = LastestArticlesFeed.description

