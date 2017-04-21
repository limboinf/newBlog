# 博客
线上地址:[http://beginman.sinaapp.com/](http://beginman.sinaapp.com/)

一个django开发的博客.网址[http://beginman.sinaapp.com/](http://beginman.sinaapp.com/).  ||  [Github](https://github.com/BeginMan/newBlog)

搭建在新浪SAE上，Clone一份改改setting里面就能运行本地，上传新浪sae上同步数据库里面就能在线展示。所有需要的第三方库都在site-packages文件夹中，可以将此内容copy到本地环境site-packages中，就可以用了。

## 开发环境
Python 2.7

Django 1.5.5

Mysql 5.5

Boostrap

## 功能
1.写博(基于Markdown编辑器)

2.上传博客（将.md文件上传后自动生成博客，如限在github搭建博客将此同步到这里或本地撰写上传。）

3.wiki功能

4.相册功能（图片上传uploadfy, 上传至七牛云存储（七牛SDK），lazyload加载）

5.关于/简历 单页。

6.命令行发送博客 [地址Github](https://github.com/BeginMan/pytool/blob/master/spider/autoSendSaeBlog.py)

## 注意：
setting配置中，由于对七牛云存储进行封装，更改你的七牛云存储Key，name即可。

## 预览

![](http://images.cnblogs.com/cnblogs_com/BeginMan/486940/o_blog1.png)

![](http://images.cnblogs.com/cnblogs_com/BeginMan/486940/o_blog2.png)

![](http://images.cnblogs.com/cnblogs_com/BeginMan/486940/o_blog3.png)

![](http://images.cnblogs.com/cnblogs_com/BeginMan/486940/o_blog4.png)

![](http://images.cnblogs.com/cnblogs_com/BeginMan/486940/o_blog5.png)

![](http://images.cnblogs.com/cnblogs_com/BeginMan/486940/o_blog6.png)

![](http://images.cnblogs.com/cnblogs_com/BeginMan/486940/o_blog7.png)

![](http://images.cnblogs.com/cnblogs_com/BeginMan/486940/o_blog8.png)
