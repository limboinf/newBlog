#coding=utf-8
__author__ = 'beginman'
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from mysite.models import Blog

class LatestEntriesFeed(Feed):
    title = u"BeginMan的技术博客"            # title
    link = "http://blog.beginman.cn/"       # 首页链接
    feed_url='http://blog.beginman.cn/'
    feed_guid='http://blog.beginman.cn/'
    author_name='BeginMan'
    description = "在学习,实践中总结和分享Python,Django,Linux,Shell,Redis,Js,web,软件设计等技术."

    def items(self):
        """数据源对象"""
        return Blog.objects.filter(is_show__isnull=True).order_by('-add_date')[:10]       # 订阅最新10篇

    def item_title(self, item):
        """数据源标题"""
        return item.title

    def item_description(self, item):
        """数据源内容"""
        return item.rss

    def item_link(self, item):
        """数据源链接地址"""
        return 'http://blog.beginman.cn'+reverse('blog', args=[item.id])

    def item_categories(self, item):
        """数据源分类"""
        return  (item.getType().name, )

    def get_absolute_url(self):
        return 'http://blog.beginman.cn/'