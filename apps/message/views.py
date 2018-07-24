from django.shortcuts import render, HttpResponse
from myWeb.adapter import Ajax, Method
import json


def message_list(request):
    param = {'articleId': request.GET.get('articleId'), "pageNum": "1", "pageSize": "50"}
    result = Ajax.connect('/message/list', Method.GET, param)
    if result.get('success'):
        return render(request, 'page/message_template.html', {'ret': result.get('data')})


def message_add(request):
    article, name, email, message, quote = request.POST.get('articleId'), \
                                           request.POST.get('name'), \
                                           request.POST.get('email'), \
                                           request.POST.get('message'), \
                                           request.POST.get('quote')

    param = {'articleId': article, 'name': name, 'email': email, 'message': message, 'quote': quote}
    if not quote.strip():
        del param['quote']
    result = Ajax.connect('/message/new', Method.POST, param)
    return HttpResponse(json.dumps(result), content_type="application/json")
