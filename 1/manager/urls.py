# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('manager.views',
    url(r'^$', 'manage', name='manage'),                # M
    url(r'^add/$', 'addBlog', name='add'),                  # A
    url(r'^upload/$', 'uploadBlog', name='uploadBlog'),                  # A
    url(r'^add_type/$', 'addType', name='add_type'),            # T
    url(r'^user/pwd/$', 'changePwd', name='changePwd'),             #PWD
    url(r'^blog/del/$', 'delBlog', name='delBlog'),                 # Delblog

    url(r'^pic/create_type/$', 'CreatePicType', name='CreatePicType'),  # create type
    url(r'^pic/upload_my_pic/(?P<id>\d+)/$', 'UploadMyPic', name='UploadMyPic'),  # up mypic
    url(r'^pic/upload/$', 'UploadPic', name='UploadPic'),  # upload
    url(r'^pic/edit_mypic/$', 'edit_mypic', name='edit_mypic'), # pic edit
)

