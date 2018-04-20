# _*_ coding:utf-8 _*_
__author__ = 'ankang'
__date__ = '2018/4/19 上午 8:56'
from django.shortcuts import render_to_response


def page_not_found(request):
    return render_to_response('404.html')


def server_inner_error(request):
    return render_to_response('500.html')
