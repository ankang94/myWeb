from django.shortcuts import render
from apps.article.models import Article
from django.utils.safestring import mark_safe


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
    qryparam = request.GET.get('group')
    if qryparam is None:
        qryparam = request.GET.get('date')

    if qryparam is None:
        qryparam = u'杂记'

    catlist = []
    if type(qryparam) == str:
        catlogs = Article.objects.filter(group__comment=qryparam).all()
    else:
        catlogs = Article.objects.filter(createdate=qryparam).all()
    for qrySet in catlogs:
        catlist.append({'title': qrySet.title,
                        'comment': qrySet.comment,
                        'date': qrySet.createdate,
                        'index': qrySet.articleid})
    return render(request, 'page/catlog.html', {'catlog': catlist, 'group': qryparam})
