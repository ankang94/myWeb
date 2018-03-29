# _*_coding:utf-8_*_
from django.db import models


# Create your models here.


class ArticleGroup(models.Model):
    groupid = models.IntegerField(verbose_name=u'类型Id', primary_key=True)
    comment = models.CharField(verbose_name=u'注释', max_length=255)

    class Meta:
        verbose_name = u'文章类型'
        verbose_name_plural = verbose_name
        db_table = u'article_group'


class Article(models.Model):
    articleid = models.IntegerField(verbose_name=u'文章Id', primary_key=True)
    groupid = models.ForeignKey(ArticleGroup)
    title = models.CharField(max_length=255, verbose_name=u'标题', default='')
    comment = models.CharField(max_length=255, verbose_name=u'副标题', null=True, blank=True)
    context = models.TextField(verbose_name=u'文章内容', null=True, blank=True)
    createdate = models.DateField(max_length=100, verbose_name=u'文章创建日期', auto_now=True)

    class Meta:
        verbose_name = u'文章库'
        verbose_name_plural = verbose_name
        db_table = u'article'
