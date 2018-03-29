from django.shortcuts import render
from apps.article.models import Article


# Create your views here.
def home(request, param):
    index = 1
    if param.isdigit():
        index = param
    atricle = Article.objects.get(articleid=index)
    result = {'title': atricle.title,
              'comment': atricle.comment,
              'article': atricle.context,
              'group': atricle.groupid.comment,
              'date': atricle.createdate}
    return render(request, 'index.html', {'dict': result})
