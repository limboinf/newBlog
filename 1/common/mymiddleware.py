#coding=utf-8
#中间件扩展
__author__ = 'beginman'
from django.http import HttpResponseRedirect
from django.conf import settings

LOGIN_URLS = ['/manage/']
ANONYMOUS_URLS = ['/manage/userGreat/', '/manage/user/']

class Mymiddleware(object):
    def process_request(self, request):
        """Request预处理函数"""
        path = str(request.path)
        request.session['domain'] = settings.DOMAIN
        if path.startswith('/site_media/'):
            return None
        #验证登陆
        if request.user.is_anonymous():
            for obj in ANONYMOUS_URLS:
                if path.startswith(obj):
                    return None

            for obj in LOGIN_URLS:
                if path.startswith(obj):
                    return HttpResponseRedirect('/login/?url=%s' % path)


