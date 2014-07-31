# coding=utf-8
from django.shortcuts import render
import urllib2
import urllib
import sys
import cookielib
from django.core.cache import cache
import simplejson as json
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')


user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0'
headers = {'User-Agent' : user_agent}




def learnEnglish(request):
    """everyday english"""
    context = {}
    if cache.get('words', None):
        context['words'] = cache.get('words')
    else:
        words = getWordsUrl()
        context['words'] = words
        cache.set('words', words, 60*60*20)
    return render(request, 'english/index.html', context)


def getWordsUrl():
    url = "http://news.iciba.com/wap/?c=index&m=more&type=show&catid=487"
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'Reason: ', e
        elif hasattr(e, 'code'):
            print 'Code: ', e
    else:
        html_doc = response.read()
        soup = BeautifulSoup(html_doc)
        remoteUrls = soup.find_all("ul")[0].find_all('a')[0]
        rurl = "http://news.iciba.com/wap/"+remoteUrls['href']  # 最新一条url
        return getWords(rurl)


def getWords(url):
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'Reason: ', e
        elif hasattr(e, 'code'):
            print 'Code: ', e
    else:
        html_doc = response.read()
        soup = BeautifulSoup(html_doc)
        remoteTxt = str(soup.find("div", class_="content"))
        return remoteTxt
