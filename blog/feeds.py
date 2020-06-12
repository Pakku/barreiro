from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html

from blog.models import Post


class LatestPostsFeed(Feed):
    title = 'Barreiro Blog'
    link = ''
    description = 'Nuevos posts de mi blog'

    def items(self):
        return Post.objects.filter(status=1)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(item.content, 30)