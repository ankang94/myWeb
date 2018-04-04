# _*_coding:utf-8_*_
from django.db import models
from myWeb import settings
import os


# Create your models here.


class ArticleGroup(models.Model):
    groupid = models.IntegerField(verbose_name=u'类型', primary_key=True)
    parentid = models.ForeignKey('self', blank=True, null=True)
    comment = models.CharField(verbose_name=u'注释', max_length=255, default='')

    class Meta:
        verbose_name = u'文章类型'
        verbose_name_plural = verbose_name
        db_table = u'article_group'

    def __str__(self):
        return self.comment


class Script(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'名称', default='')
    path = models.CharField(max_length=255, verbose_name=u'脚本路径', default='')
    type = models.CharField(max_length=2, choices=(('C', u'css脚本'), ('J', u'js脚本')), verbose_name=u'脚本类型', default='')

    class Meta:
        verbose_name = u'脚本'
        verbose_name_plural = verbose_name
        db_table = u'rela_script'

    def __str__(self):
        return self.name


class Image(models.Model):
    path = models.ImageField(upload_to='%Y/%m/%d/', verbose_name=u'图片')

    class Meta:
        verbose_name = u'图片'
        verbose_name_plural = verbose_name
        db_table = u'images'

    def __str__(self):
        return str(self.path).split('/')[-1]


class Article(models.Model):
    articleid = models.AutoField(verbose_name=u'文章Id', primary_key=True)
    group = models.ForeignKey('ArticleGroup', verbose_name=u'类型')
    title = models.CharField(max_length=255, verbose_name=u'标题', default='')
    comment = models.CharField(max_length=255, verbose_name=u'副标题', null=True, blank=True)
    context = models.TextField(verbose_name=u'文章内容', null=True, blank=True)
    createdate = models.DateField(max_length=100, verbose_name=u'文章创建日期', auto_now=True)
    script = models.ManyToManyField('Script', verbose_name=u'需要的脚本', blank=True)
    image = models.ManyToManyField('Image', verbose_name=u'blog图片', blank=True)

    class Meta:
        verbose_name = u'文章库'
        verbose_name_plural = verbose_name
        db_table = u'article'

    def __str__(self):
        return '{0}({1})'.format(self.title, self.comment)
