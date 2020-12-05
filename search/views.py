from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from pypinyin import *
from search.models import *


def update(request):
    data = json.loads(request.body)
    aid = data.get("administratorid")
    fpath = data.get("filepath")
    filename = fpath[fpath.rfind("\\")+1::]
    sline = data.get("startline")
    alines = data.get("linesnumber")
    ul = Update_Log.objects.create(filename=filename, updateadministrator_id=aid,
                              startlinenum=sline, finishlinenum=sline+alines)

    ufile = open(fpath, "r", 10)
    for line in ufile.readlines()[sline-1:(sline+alines-1)]:
        print(line)

    ufile.close()

    return JsonResponse({
        "status": 0,
        "message": "update success"
    })


def associatetoAuthor(request):
    data = json.loads(request.body)
    name_zh = data.get("name")
    sytle = Style.NORMAL
    name = pinyin(name_zh, sytle)
    print(name)

    return JsonResponse({
        "status": 0,
        "message": "update success"
    })