# _*_coding:utf-8_*_
from django.db import models


# Create your models here.
class CopyArticle(models.Model):
    name = models.CharField(verbose_name=u'站点名', max_length=40, default='')
    host = models.CharField(verbose_name=u'站点Host', max_length=40, primary_key=True)
    title = models.CharField(verbose_name=u'文章标题', max_length=100, default='')
    h2 = models.CharField(verbose_name=u'导航标题1', max_length=100, blank=True)
    h3 = models.CharField(verbose_name=u'导航标题2', max_length=100, blank=True)
    context = models.CharField(verbose_name=u'内容', max_length=100, default='')
    code = models.CharField(verbose_name=u'代码', max_length=100, blank=True)
    exclude = models.CharField(verbose_name=u'排除', max_length=100, blank=True)

    class Meta:
        verbose_name = u'拷贝模板'
        verbose_name_plural = verbose_name
        db_table = u'copy_template'

    def __str__(self):
        return self.name


class CopyLogin(models.Model):
    host = models.OneToOneField('CopyArticle', verbose_name=u'站点', primary_key=True, db_column='host')
    username = models.CharField(verbose_name=u'用户名', max_length=40, default='')
    password = models.CharField(verbose_name=u'密码', max_length=40, default='')
    signal = models.CharField(verbose_name=u'等待标识', max_length=40, default='')
    js = models.CharField(verbose_name=u'登陆脚本', max_length=2000, default='')
    cookie = models.CharField(verbose_name=u'Cookie名', max_length=40, default='')

    class Meta:
        verbose_name = u'模拟登陆'
        verbose_name_plural = verbose_name
        db_table = u'copy_login'

    def __str__(self):
        return self.host
