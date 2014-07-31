# coding=utf-8
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mysite.views.home', name='home'),                   # 首页
    url(r'^about/$', 'mysite.views.about', name='about'),                   # about
    url(r'^resume/$', 'mysite.views.resume', name='resume'),                   # contact
    url(r'^manage/', include('manager.urls')),                      # manager
)

# Serve static files for admin, use this for debug usage only
# `python manage.py collectstatic` is preferred.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from common.rss import LatestEntriesFeed
urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)


urlpatterns += patterns('mysite.views',
    url(r'^login/$', 'login_', name='login'),                           # 登陆
    url(r'^logout/$', 'logout_', name='logout'),                        # 登出
    url(r'^blog/(?P<id>\d+)/$', 'blog', name='blog'),                        # 正文
    url(r'^blog/search/$', 'search', name='search'),                    # 检索
    url(r'^blog/common/$', 'sidebar', name='sidebar'),                  # 侧栏异步加载
    url(r'^blog/type/(?P<id>\d+)/$', 'blogType', name='blogType'),      # 博客类型检索
    url(r'^blog/tag/(?P<id>\d+)/$', 'blogTag', name='blogTag'),         # 博客标签检索


    url(r'^wiki/$', 'wiki', name='wiki'),                               # 维基百科
    url(r'^wiki/(?P<id>\d+)/$', 'wiki', name='wiki'),                               # 维基百科
    url(r'^wiki/add_type/$', 'wiki_add_type', name='wiki_add_type'),    # 维基百科添加分类
    url(r'^wiki/add/(?P<id>\d+)/$', 'wiki_add', name='wiki_add'),    # 维基百科添加
    url(r'^common/del/$', 'commonDel', name='commonDel'),               # del

    url(r'^pic/$', 'pic', name='pic'),          # 图片首页
    url(r'^pic/(?P<id>\d+)/$', 'picView', name='picView'),          # 图片
    url(r'^feed/$', LatestEntriesFeed()),
    url(r'^pigeonhole/$', 'pigeonhole', name='pigeonhole'),          # 归档
    url(r'^ciphertext/(?P<id>\d+)/$', 'ciphertext', name='ciphertext'),          # 密文

)

#接口数据
urlpatterns += patterns('mysite.views',
    url(r'^api/category/$', 'getCategory', name='getCategory'),         # 获取分类
    url(r'^api/tag/$', 'getTag', name='getTag'),                        # 获取标签
)


#english
urlpatterns += patterns('mysite.english',
    url(r'^english/$', 'learnEnglish', name='learnEnglish'),         # english index
)