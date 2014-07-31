#coding=utf-8
from django import forms
from django.forms import ModelForm
import random
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from mysite.models import Type, Blog, Wiki, PicType, MyPic
from PIL import Image
import string
from wmd.widgets import MarkDownInput   # 从wmd编辑器导入html组件


class LoginForm(forms.Form):
    """
    ===============================================================================
    function：    表单登录类
    developer:    BeginMan
    add-time      2014/6/3
    ===============================================================================
    """
    us = forms.CharField(label=u'用户名',max_length=100,widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': u'用户名', 'required': '', 'autofocus': ''}
        ),
    )
    pwd = forms.CharField(label=u'密码',widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': u'密码', 'required': ''}
        )
    )
    auto_login = forms.BooleanField(label=u'记住密码',required=False,
        widget=forms.CheckboxInput(attrs={'value': 1}),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        self.auth_login = None
        super(LoginForm, self).__init__(*args, **kwargs)


    def clean(self):
        us = self.cleaned_data.get('us')
        password = self.cleaned_data.get('pwd')
        auth_login = self.cleaned_data.get('auth_login', None)

        if us and password:
            if not User.objects.filter(username=us).exists():
                raise forms.ValidationError(u'该账号不存在')

            self.user_cache = authenticate(username=us, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'邮箱或密码错误！')

            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'该帐号已被禁用！')


        if auth_login:      # 如果用户勾选了自动登录
            self.auth_login = True

        return self.cleaned_data

    def get_user_id(self):
        """获取用户id"""
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        """获取用户实例"""
        return self.user_cache

    def get_auto_login(self):
        """是否勾选了自动登录"""
        return self.auth_login

    def get_user_is_first(self):
        """获取用户是否是第一次登录"""
        is_first = False
        if self.user_cache and self.user_cache.type == -1:
            is_first = True
            self.user_cache.save()
        return is_first




class PasswordForm(forms.Form):
    """
    ===============================================================================
    function：    用户修改密码
    developer:    BeginMan
    add-time      2014/6/3
    ===============================================================================
    """
    oldpwd = forms.CharField(label=u'原始密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': u'原始密码', 'required': ''})
    )
    password1 = forms.CharField(label=u'新密码', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': u'密码长度在5-12位', 'required': ''})
    )
    password2 = forms.CharField(label=u'在输入一次', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': u'在输入一次', 'required': ''})
    )

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        self.newpwd = None
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        oldpwd = cleaned_data.get("oldpwd")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if not self.user.check_password(oldpwd):
            msg = u"原密码错误。"
            self._errors["oldpwd"] = self.error_class([msg])
            # raise forms.ValidationError(u'原密码错误')
        if password1 and password2:
            if password1 != password2:
                msg = u"两个密码字段不一致。"
                self._errors["password2"] = self.error_class([msg])
            if not 4 < len(password1) < 13:
                msg = u"密码要在5-12位之间。"
                self._errors["password1"] = self.error_class([msg])

        return cleaned_data




class BlogForm(ModelForm):
    """add blog"""
    title = forms.CharField(max_length=100, label=u'标题', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'标题', 'required': ''})
    )
    type = forms.IntegerField()
    is_show = forms.CharField(required=False, max_length=100, label=u'加密', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'密码'})
    )
    content = forms.CharField(label=u'内容',widget=MarkDownInput(
        attrs={'class': 'form-control', 'placeholder': u'内容', 'required': ''})
    )

    class Meta:
        model = Blog
        fields = ('title','type', 'content', 'is_show')


class WikiForm(ModelForm):
    """add wiki"""
    content = forms.CharField(label=u'wiki',widget=MarkDownInput(
        attrs={'class': 'form-control', 'placeholder': u'wiki', 'required': ''})
    )
    class Meta:
        model = Wiki
        fields = ('content',)



class PicTypeForm(ModelForm):
    """pictype form"""
    title = forms.CharField(max_length=100, label=u'title', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': u'title', 'required': ''})
    )
    desc = forms.CharField(label=u'wiki',widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': u'describe'})
    )

    def clean(self):
        cleaned_data = super(PicTypeForm, self).clean()
        title = cleaned_data.get('title').strip()

        if not title and PicType.objects.filter(title__icontains=title).exists():
            raise forms.ValidationError(u'该分类已存在')
        return cleaned_data

    class Meta:
        model = PicType
        fields = ('title', 'desc')


class MypicForm(ModelForm):
    """MypicForm form"""
    type = forms.ModelChoiceField(queryset=PicType.objects.order_by('-id'), widget=forms.RadioSelect)
    desc = forms.CharField(label=u'wiki',widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': u'describe'})
    )

    class Meta:
        model = MyPic
        fields = ('type', 'desc')