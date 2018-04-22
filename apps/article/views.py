from django.shortcuts import render
from apps.article.models import Article, ArticleGroup
from django.utils.safestring import mark_safe
import datetime, json
from article.utils import parsetitles, Cache, parsetabs, parsesource, generatepage
from django.shortcuts import render_to_response


# Create your views here.
def gettitle():
    if not Cache().get('titles'):
        Cache('titles', ArticleGroup.objects.all())
    return Cache().get('titles')


def article(request, gid, aid):
    grouoplist = parsetitles(gettitle(), int(gid))
    articles = Article.objects.get(articleid=int(aid))
    if not articles:
        return render_to_response('404.html')

    cd = articles.createdate.strftime("%Y%m%d%H%M%S")
    ms_key = '{0}_ms_{1}'.format(aid, cd)
    cach_ms = Cache().get(ms_key)
    if cach_ms:
        ms = cach_ms
    else:
        ms = mark_safe(articles.context)
        Cache(ms_key, ms, 60 * 60 * 12)

    result = {'title': articles.title,
              'comment': articles.comment,
              'summary': articles.summary,
              'article': ms,
              'groupid': articles.group.groupid,
              'date': articles.createdate}

    parsesource(articles, result)
    tabs = parsetabs(Cache().get('titles'), result)
    return render(request, 'page/container.html', {'dict': result, 'titles': grouoplist, 'tabs': tabs})


def catlog(request, gid, pid):
    qrydate = request.GET.get('d')

    if not gid or not gid.strip():
        gid = 0
    if not pid or not pid.strip():
        pid = 1

    grouoplist = parsetitles(gettitle(), int(gid))

    if not qrydate:
        catlogs = Article.objects.filter(group__groupid=gid).all()
    else:
        try:
            qrydate = datetime.datetime.strptime(qrydate, '%Y-%m-%d')
            catlogs = Article.objects.filter(group__groupid=gid,
                                             createdate__year=qrydate.year,
                                             createdate__month=qrydate.month,
                                             createdate__day=qrydate.day).all()
        except ValueError:
            catlogs = Article.objects.filter(group__comment=gid).all()

    ret = generatepage(catlogs, pid)

    param = {'groupid': gid}
    if qrydate:
        param['date'] = qrydate
    tabs = parsetabs(gettitle(), param)
    return render(request, 'page/catlog.html',
                  {'catlog': ret.get('list'), 'titles': grouoplist,
                   'tabs': tabs, 'pages': ret.get('page')})


def search(request, pid):
    param = request.GET.get('qrm')
    if not pid or not pid.strip():
        pid = 1
    grouoplist = [{'comment': '搜索', 'state': 'active'}]
    grouoplist.extend(parsetitles(gettitle()))
    if not param or not param or not param.strip():
        return render(request, 'page/catlog.html', {'titles': grouoplist,
                                                    'qrm': param,
                                                    'tabs': [{'title': 'Search'}],
                                                    'pages': json.dumps({'current': 1, 'total': 1})})
    catlogs = Article.objects.filter(title__icontains=param).all()
    ret = generatepage(catlogs, pid)

    return render(request, 'page/catlog.html', {'titles': grouoplist,
                                                'qrm': param,
                                                'tabs': [{'title': 'Search'}],
                                                'catlog': ret.get('list'),
                                                'pages': ret.get('page')})
