from django.shortcuts import render
from apps.article.models import Article, ArticleGroup
from django.utils.safestring import mark_safe
import datetime
from .utils import parsetitles, Cache


# Create your views here.
def article(request, param):
    index = 1
    if param.isdigit():
        index = param
    atricle = Article.objects.get(articleid=index)
    result = {'title': atricle.title,
              'comment': atricle.comment,
              'article': mark_safe(atricle.context),
              'group': atricle.group.comment,
              'date': atricle.createdate}
    return render(request, 'page/container.html', {'dict': result})


def catlog(request, qrygroup):
    qrydate = request.GET.get('date')

    catlist = []

    if not qrygroup or not qrygroup.strip():
        qrygroup = 0
    if not Cache().get('titles'):
        Cache('titles', ArticleGroup.objects.all())
    grouoplist = parsetitles(Cache().get('titles'), int(qrygroup))

    if qrydate is None:
        catlogs = Article.objects.filter(group__groupid=qrygroup).all()
    else:
        try:
            qrydate = datetime.datetime.strptime(qrydate, '%Y-%m-%d')
            catlogs = Article.objects.filter(group__groupid=qrygroup,
                                             createdate__year=qrydate.year,
                                             createdate__month=qrydate.month,
                                             createdate__day=qrydate.day).all()
        except:
            catlogs = Article.objects.filter(group__comment=qrygroup).all()

    for qrySet in catlogs:
        catlist.append({'title': qrySet.title,
                        'comment': qrySet.comment,
                        'date': qrySet.createdate,
                        'index': qrySet.articleid})
    return render(request, 'page/catlog.html', {'catlog': catlist, 'titles': grouoplist})
