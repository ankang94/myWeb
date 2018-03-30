from django.shortcuts import render
from apps.article.models import Article
from django.utils.safestring import mark_safe
import datetime


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


def catlog(request):
    qryparam = request.GET.get('param_group')
    if qryparam is None:
        qryparam = request.GET.get('param_date')

    catlist = []

    if qryparam is None or qryparam == u'所有':
        qryparam = u'所有'
        catlogs = Article.objects.all()
    else:
        try:
            qrydate = datetime.datetime.strptime(qryparam, '%Y-%m-%d')
            catlogs = Article.objects.filter(createdate__year=qrydate.year,
                                             createdate__month=qrydate.month,
                                             createdate__day=qrydate.day).all()
        except:
            catlogs = Article.objects.filter(group__comment=qryparam).all()

    for qrySet in catlogs:
        catlist.append({'title': qrySet.title,
                        'comment': qrySet.comment,
                        'date': qrySet.createdate,
                        'index': qrySet.articleid})
    return render(request, 'page/catlog.html', {'catlog': catlist, 'group': qryparam})
