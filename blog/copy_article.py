from models import Article, Articles_deamon

def copy_article():
    old_article_list = Article.objects.all()
    
    for article in old_article_list:
            Articles_deamon.objects.create(title=article.title, body=article.body, summary=article.summary,
                                          publish_date=article.publish_date, status=article.status, 
                                           enable_comment=article.enable_comment, author=article.author,
                                          tags=article.tags, categories=article.categories, slug=article.slug)

if __name__ == '__main__':
        copy_article()
