from django.shortcuts import render
from apps.article.models import Article, ArticleGroup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe
import datetime, json
from .utils import parsetitles, Cache, parsetabs, parsesource


# Create your views here.
def article(request, gid, aid):
    if not Cache().get('titles'):
        Cache('titles', ArticleGroup.objects.all())
    grouoplist = parsetitles(Cache().get('titles'), int(gid))
    articles = Article.objects.get(articleid=int(aid))

    result = {'title': articles.title,
              'comment': articles.comment,
              'article': mark_safe(articles.context),
              'groupid': articles.group.groupid,
              'date': articles.createdate}

    parsesource(articles, result)
    tabs = parsetabs(Cache().get('titles'), result)
    return render(request, 'page/container.html', {'dict': result, 'titles': grouoplist, 'tabs': tabs})


def catlog(request, gid, pid):
    qrydate = request.GET.get('d')

    catlist = []

    if not gid or not gid.strip():
        gid = 0
    if not pid or not pid.strip():
        pid = 1
    if not Cache().get('titles'):
        Cache('titles', ArticleGroup.objects.all())
    grouoplist = parsetitles(Cache().get('titles'), int(gid))

    if not qrydate:
        catlogs = Article.objects.filter(group__groupid=gid).all()
    else:
        try:
            qrydate = datetime.datetime.strptime(qrydate, '%Y-%m-%d')
            catlogs = Article.objects.filter(group__groupid=gid,
                                             createdate__year=qrydate.year,
                                             createdate__month=qrydate.month,
                                             createdate__day=qrydate.day).all()
        except:
            catlogs = Article.objects.filter(group__comment=gid).all()

    paginator = Paginator(catlogs, 20)

    try:
        catlogs = paginator.page(int(pid))
    except PageNotAnInteger:
        catlogs = paginator.page(1)
    except EmptyPage:
        catlogs = paginator.page(paginator.num_pages)

    pageparam = json.dumps({'current': pid, 'total': paginator.num_pages})

    for qrySet in catlogs:
        catlist.append({'title': qrySet.title,
                        'comment': qrySet.comment,
                        'date': qrySet.createdate,
                        'url': '/g' + str(gid) + '/a' + str(qrySet.articleid)})

    param = {'groupid': gid}
    if qrydate:
        param['date'] = qrydate
    tabs = parsetabs(Cache().get('titles'), param)
    return render(request, 'page/catlog.html',
                  {'catlog': catlist, 'titles': grouoplist, 'tabs': tabs, 'pages': pageparam})
