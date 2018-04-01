# _*_coding:utf-8_*_
__author__ = 'ankang'
__date__ = '2018/03/31 21:12'
import time


# common tools for article

def createtabs(pdict):
    rlist = []
    if pdict.group.comment is not None:
        rlist.append({'group': pdict.group.comment,
                      'url': '/?group=' + pdict.group.groupid})
    if pdict.createdate is not None:
        rlist.append({'date': pdict.createdate,
                      'url': '/?date=' + pdict.createdate.strftime('%Y-%m-%d')})


def parsetitles(pset, group):
    rlist = []
    plist = []
    for item in pset:
        param = {'titles': [],
                 'groupid': item.groupid,
                 'comment': item.comment,
                 'parentid': item.parentid,
                 'url': '/?group=' + str(item.groupid)}
        if item.groupid == group:
            param['state'] = 'active'
        plist.append(param)

    for item in plist:
        if item.get('parentid') is None:
            rlist.append(item)

    for item in plist:
        if item in rlist:
            continue
        pitem = finditembyid(rlist, item.get('parentid').groupid)
        if pitem is not None:
            pitem['type'] = 'muilt'
            pitem['titles'].append(item)

    return rlist


def parsetabs():
    pass


def finditembyid(targetlist, targetid):
    for item in targetlist:
        if item.get('groupid') == targetid:
            return item
    return None
