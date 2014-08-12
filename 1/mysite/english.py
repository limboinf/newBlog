# coding=utf-8
from django.shortcuts import render
import urllib2
import urllib
from mysite.models import Word, Words
from common.form import WordsForm
import sys
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
import cookielib
from django.core.cache import cache
import simplejson as json
import platform
import datetime
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')
import pylibmc as memcache
mc = memcache.Client()


user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0'
headers = {'User-Agent' : user_agent}
API_KEY = '1554050065'
KEYFORM = 'BeginMan'



def learnEnglish(request):
    """everyday english"""
    context = {}
    if mc.get('sequence'):
        context['words'] = mc.get('sequence')
    else:
        words = getWordsUrl()
        context['words'] = words
        mc.set("sequence", words, time=60*60*24)
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


def words(request):
    """words index"""
    context = {}
    now = datetime.datetime.now().date()
    context['now'] = now
    if mc.get('word') and mc.get('words'):
        context['word'] = mc.get('word')
        context['mywords'] = mc.get('words')

    else:
        word = Word.objects.all().order_by('-id')
        if word:
            word = word[0]
            mc.set('word', word, time=60*60*24)
            context['word'] = word
            mywords = Words.objects.filter(word=word, status=0)
            mc.set('mywords', mywords, time=60*60*24)
            context['mywords'] = mywords
    return render(request, 'english/words.html', context)


def has_done(request):
    context = {}
    now = datetime.datetime.now().date()
    context['now'] = now
    if mc.get('word') and mc.get('words'):
        context['word'] = mc.get('word')
        context['mywords'] = mc.get('words')

    else:
        word = Word.objects.all().order_by('-id')
        if word:
            word = word[0]
            mc.set('word', word, time=60*60*24*10)
            context['word'] = word
            mywords = Words.objects.filter(word=word, status=1).order_by('-id')
            mc.set('mywords', mywords, time=60*60*24*10)
            context['mywords'] = mywords
    return render(request, 'english/has_done_words.html', context)


@login_required(login_url='/login/')
def add_edit_words(request, type=0, id=0):
    """type:0 add; 1:edit"""
    context = {}
    id = int(id)
    type = int(type)   # word主记录 id
    if id:
        obj = Words.objects.get(pk=id)
    if request.method == 'POST':
        f = WordsForm(request.POST, instance=obj) if id else WordsForm(request.POST)
        if f.is_valid():
            english = f.cleaned_data['english']
            if not type:
                type = Word.objects.create().id
            ff = f.save(commit=False)
            ff.word_id = type
            explains = Sjson(GetTranslate(english))
            ff.explain = explains[1]
            ff.phonetic = explains[0]
            ff.seq = explains[2]
            ff.save()
            return  HttpResponseRedirect('/english/word/')
        context['f'] = f

    f = WordsForm(instance=obj) if id else WordsForm()
    context['id'] = id
    context['f'] = f

    return render(request, 'english/add.html', context)



def GetTranslate(txt):
    url = 'http://fanyi.youdao.com/openapi.do'
    data = {
        'keyfrom': KEYFORM,
        'key': API_KEY,
        'type': 'data',
        'doctype': 'json',
        'version': 1.1,
        'q': txt
	}
    data = urllib.urlencode(data)
    url = url+'?'+data
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    result = json.loads(response.read())
    return result

def Sjson(json_data):
    query = json_data.get('query','')				# 查询的文本
    translation = json_data.get('translation','') 	# 翻译
    basic = json_data.get('basic','')				# basic 列表
    sequence = json_data.get('web',[])				# 短语列表
    phonetic,explains_txt,seq_txt = '','',''

    # 更多释义
    if basic:
        phonetic = basic.get('phonetic','')			# 音标
        explains = basic.get('explains',[])			# 更多释义 列表
        for obj in explains:
            explains_txt += obj+'<br/>'

    # 句子解析
    if sequence:
        for obj in sequence:
            seq_txt += obj['key']+'<br/>'
            values = ''
            for i in obj['value']:
                values += i+','
            seq_txt += values+'<br/>'
    return (phonetic, explains_txt, seq_txt)


def done(request):
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        type = request.POST.get('type', 0)
        if int(type) == 1:
            Words.objects.filter(id=id).update(status=1)
        else:
            Words.objects.filter(id=id).update(status=0)
        return HttpResponse('ok')