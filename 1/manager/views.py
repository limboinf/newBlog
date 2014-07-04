# coding=utf-8
from django.shortcuts import render
from common.form import BlogForm,PasswordForm, PicTypeForm, MypicForm
from django.http import HttpResponseRedirect, HttpResponse
from mysite.models import Type, Tag, Blog, BlogTag, PicType, Pic, MyPic
from django.shortcuts import get_object_or_404
from common import ajax
import simplejson as json
import datetime
import random
import re, string
from common.superqiniu import SuperQiniu
from BeautifulSoup import BeautifulSoup
from markdown import markdown

def manage(request):
    """后台"""
    context = {}
    user = request.user

    return render(request, 'manager/manage.html', context)




def addBlog(request):
    """add blog"""
    context = {}
    now = datetime.datetime.now()
    user = request.user
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            title = formData.get('title')
            content = formData.get('content')
            type = formData.get('type')
            tags = request.POST.get('id_tag', '')
            obj = int(request.POST.get('edit_or_creat'))    # 编辑还是创建
            now = datetime.datetime.now()
            # 保存theme
            # 将markdown格式转换纯文本

            from markdown import markdown
            html = markdown(content)
            if len(content) > 500:
                html = markdown(content[:500])
            summary = ''.join(BeautifulSoup(html).findAll(text=True))

            if obj:     # 编辑状态
                blog = Blog.objects.filter(id=obj).update(title=title, type=int(type), summary=summary, content=content, add_date=now)
                blog = Blog.objects.get(id=obj)
            else:
                blog = Blog.objects.create(
                    title=title, type=int(type), summary=summary, content=content, add_date=now
                )
            # 博客导图
            img = getPic(blog.content_show)
            blog.img = img
            blog.save()

            if tags:
                tags = json.loads(tags)
                tag_list = []
                for i in tags:
                    i = i.strip()
                    if i and not Tag.objects.filter(name__iexact=i).exists():
                        tag = Tag.objects.create(name=i)
                        tag_list.append(tag)
                    elif i:
                        tag_list.append(Tag.objects.filter(name__iexact=i)[0])

                if obj:     # 编辑状态
                    BlogTag.objects.filter(blog=blog).delete()
                # 创建ThemeTag
                for i in tag_list:
                    BlogTag.objects.create(blog=blog, tag=i)
            return HttpResponseRedirect('/')

        context['form'] = form
        return render(request, 'manager/addtheme.html', context)
    else:
        id = request.GET.get('id', None)
        context['form'] = BlogForm()
        is_edit = 0
        if id:      # 编辑状况
            is_edit = id
            blog = get_object_or_404(Blog, pk=int(id))
            context['form'] = BlogForm(instance=blog)
            context['has_tags'] = BlogTag.objects.filter(blog=blog)
        codes = Type.objects.all().order_by('-id')
        tags = Tag.objects.all().order_by('-id')
        context['codes'] = codes
        context['tags'] = tags
        context['is_edit'] = is_edit
    return render(request, 'manager/addtheme.html', context)



def uploadBlog(request):
    """Upload blog"""
    context = {}
    now = datetime.datetime.now()
    if request.method == 'POST':
        type = request.POST.get('type')
        tags = request.POST.get('id_tag', '')
        file = request.FILES.get('blog')
        context = file.read().decode('utf-8').split('---', 2)
        content = [i for i in context if i]
        head = content[0]
        body = content[1]
        title =  re.findall(r'title: .*', head)
        if title:
            title = title[0].split(':')[1].strip()
        else:
            title = u'一个神秘的标题'

        html = markdown(body)
        if len(body) > 500:
            html = markdown(body[:500])

        summary = ''.join(BeautifulSoup(html).findAll(text=True))
        blog = Blog.objects.create(
                    title=title, type=int(type), summary=summary, content=body, add_date=now
                )
        # 博客导图
        img = getPic(blog.content_show)
        blog.img = img
        blog.save()
        if tags:
            tags = json.loads(tags)
            tag_list = []
            for i in tags:
                i = i.strip()
                if i and not Tag.objects.filter(name__iexact=i).exists():
                    tag = Tag.objects.create(name=i)
                    tag_list.append(tag)
                elif i:
                    tag_list.append(Tag.objects.filter(name__iexact=i)[0])

            # 创建ThemeTag
            for i in tag_list:
                BlogTag.objects.create(blog=blog, tag=i)
        return HttpResponseRedirect('/')
    context['types'] = Type.objects.order_by('-id')
    context['tags'] = Tag.objects.order_by('-id')
    return render(request, 'manager/uploadblog.html', context)


def addType(request):
    """添加分类"""
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name').strip().lower()
        if not Type.objects.filter(name__iexact=name).exists():
            c_id = Type.objects.create(name=name).id
            return ajax.ajax_ok(c_id)



def changePwd(request):
    """更改密码"""
    context = {}
    user = request.user
    context['form'] = PasswordForm()
    if request.method == 'POST':
        form = PasswordForm(user, request.POST)
        if form.is_valid():
            newpwd = form.cleaned_data.get('password1', None)
            if newpwd:
                user.set_password(newpwd)
                user.save()
                return HttpResponseRedirect('/')
        context['form'] = form
    return render(request, 'manager/pwd.html', context)


def getPic(html):
    """获取图片"""
    soup = BeautifulSoup(html)
    s = soup.find('img')
    if s:
        return s['src']
    return '/site_media/img/blog/%s.jpg' % (random.choice(range(1, 10)))


def delBlog(request):
    """del blog"""
    if request.method == 'POST':
        id = request.POST.get('id')
        BlogTag.objects.filter(blog__id=id).delete()
        Blog.objects.filter(id=id).delete()
        return HttpResponse('ok')




def UploadPic(request):
    """upload pic to qiniu."""
    if request.method == 'POST':
        img = request.FILES.get('Filedata', None)
        type = request.POST.get('type', None)
        if type:
            qn = SuperQiniu(img, w=800, h=520)
        else:
            qn = SuperQiniu(img)
        qn.uploadFile()
        remote_url = qn.downloadFile()
        key = qn.getKey()
        pic = Pic.objects.create(img=remote_url, key=key)
        return ajax.ajax_ok({'id':pic.id, 'url':pic.img, 'key':key})



def CreatePicType(request):
    """create the type of picture"""
    context = {}
    if request.method == 'POST':
        id = int(request.POST.get('id', 0))
        if id:
            pictype =get_object_or_404(PicType, pk=id)
            form = PicTypeForm(request.POST, instance=pictype)
        else:
            form = PicTypeForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            img = request.POST.get('pid')
            f.img = img
            f.save()
            return HttpResponseRedirect('/pic/')
        context['form'] = form

    else:
        id = request.GET.get('id', None)
        form = PicTypeForm()
        if id:
            pictype =get_object_or_404(PicType, pk=id)
            context['img_obj'] = pictype.getPic()
            form = PicTypeForm(instance=pictype)
        context['form'] = form
        context['id'] = id

    return render(request, 'pic/addtype.html', context)


def UploadMyPic(request, id):
    """create the type of picture"""
    context = {}
    if request.method == 'POST':
        data = request.POST.get('data')
        data = json.loads(data)

        for obj in data:
            MyPic.objects.create(type=id, img=obj['pid'], desc=obj['desc'])
        return HttpResponse('ok')

    else:
        pictype =get_object_or_404(PicType, pk=id)
        context['pictype'] = pictype

    return render(request, 'pic/addpic.html', context)



def edit_mypic(request):
    """edit mypic"""
    if request.method == 'POST':
        id = request.POST.get('id')
        desc = request.POST.get('desc', '')
        MyPic.objects.filter(pk=id).update(desc=desc)
        return HttpResponse('ok')