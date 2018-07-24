# _*_coding:utf-8_*_
from django.db import models
from apps.article.models import Article


# Create your models here.
class Visitor(models.Model):
    name = models.CharField(verbose_name=u'昵称', max_length=255, unique=True)
    email = models.EmailField(verbose_name=u'邮箱', unique=True, db_column='email')
    ban = models.IntegerField(verbose_name=u'违规次数', db_column='ban')
    date = models.DateTimeField(verbose_name=u'时间', db_column='mb_date')

    class Meta:
        verbose_name = u'访客'
        verbose_name_plural = verbose_name
        db_table = u'mb_visitor'

    def __str__(self):
        return self.name


class Message(models.Model):
    visitor = models.ForeignKey('Visitor', verbose_name=u'访客', db_column='visitor')
    article = models.ForeignKey(Article, verbose_name=u'文章', db_column='article')
    message = models.TextField(verbose_name=u'留言', db_column='message')
    parent = models.ForeignKey('Message', related_name='quote', verbose_name=u'引用留言', blank=True, db_column='parent')
    date = models.DateTimeField(verbose_name=u'时间', db_column='mb_date')

    class Meta:
        verbose_name = u'留言板'
        verbose_name_plural = verbose_name
        db_table = u'mb_message'

    def __str__(self):
        return self.message
