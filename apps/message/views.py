from django.shortcuts import render, HttpResponse
from myWeb.adapter import Ajax, Method
import json, math


def message_list(request):
    param = {'articleId': request.GET.get('articleId'), "pageNum": request.GET.get('pageNum'), "pageSize": "10"}
    result = Ajax.connect('/message/list', Method.GET, param)
    if result.get('success'):
        pagination = result.get('data').get('pagination')
        page_max = int(math.ceil(pagination.get('total') / pagination.get('size')))
        start = pagination.get('current') / 5
        start = int(start) * 5 + 1 if start > 1 else 1
        offset = pagination.get('current') % 5
        offset = 5 if offset == 0 else offset
        end = start + 4 if start + 4 < page_max else page_max
        prev_status = 'disabled' if start in range(1, 6) else ''
        next_status = 'disabled' if end in range(page_max + offset - 5, page_max + 1) else ''
        return render(request, 'page/message_template.html', {'ret': result.get('data'),
                                                              'pages': range(start, end + 1),
                                                              'offset': offset,
                                                              'ps': prev_status,
                                                              'ns': next_status})


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
