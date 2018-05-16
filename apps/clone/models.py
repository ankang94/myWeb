from django.db import models


# Create your models here.
class CopyArticle(models.Model):
    name = models.CharField(verbose_name=u'站点名', max_length=40, default='')
    host = models.CharField(verbose_name=u'站点Host', max_length=40, default='')
    title = models.CharField(verbose_name=u'文章标题', max_length=100, default='')
    h2 = models.CharField(verbose_name=u'导航标题1', max_length=100, default='')
    h3 = models.CharField(verbose_name=u'导航标题2', max_length=100, default='')
    context = models.CharField(verbose_name=u'内容', max_length=100, default='')
    code = models.CharField(verbose_name=u'代码', max_length=100, default='')

    class Meta:
        verbose_name = u'拷贝模板'
        verbose_name_plural = verbose_name
        db_table = u'copy_template'

    def __str__(self):
        return self.name