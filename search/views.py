from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from pypinyin import *
from search.models import *
import os
import codecs
from django.core import serializers
from django.core.serializers import serialize
import operator
import chardet
from elasticsearch import Elasticsearch

# from elasticsearch._async import helpers

host_list = [
    # '49.234.51.41:9200',
    # "47.95.233.29:9200",
    # "49.234.51.41:9200",
    # "120.26.186.203:9200"
    '123.57.107.14:9200'
]


# 更新数据
def update(request):
    data = json.loads(request.body)
    aid = data.get("administratorid")
    fpath = data.get("filepath")
    filename = fpath[fpath.rfind("\\") + 1::]
    sline = data.get("startline")
    alines = data.get("linesnumber")
    ul = Update_Log.objects.create(filename=filename, updateadministrator_id=aid,
                                   startlinenum=sline, finishlinenum=sline + alines)

    ufile = open(fpath, "r", 10)

    client = Elasticsearch(host_list)
    # Authors表需要特别处理，对其中pubs对象添加isdisplay字段
    if filename.find("authors") != -1:
        for line in ufile.readlines()[sline - 1:(sline + alines - 1)]:
            line_json = json.loads(line)
            pubs = line_json["pubs"]
            for pub in pubs:
                pub["isdisplay"] = 1
            client.index(index='author', doc_type='_doc', body=line_json)

    elif filename.find("papers") != -1:
        for line in ufile.readlines()[sline - 1:(sline + alines - 1)]:
            client.index(index='paper', doc_type='_doc', body=json.loads(line))

    else:
        for line in ufile.readlines()[sline - 1:(sline + alines - 1)]:
            client.index(index='venue', doc_type='_doc', body=json.loads(line))

    ufile.close()

    return JsonResponse({
        "status": 0,
        "message": "update success"
    })


# 根据文件名获取更新记录
## 下拉框可选 一共就3种 author venue paper
## 结果按时间排序
def getupdatebyfilename(request):
    data = json.loads(request.body)
    aid = data.get("administratorid")
    filename = data.get("filename")
    record = Update_Log.objects.filter(filename__icontains=filename).all().order_by("-updatetime")
    record = serialize('json', record)
    record = json.loads(record)
    record_list = []
    for re in record:
        record_list.append(re['fields'])
    return JsonResponse(record_list, safe=False)

# 获取可认领的门户
## 未用拼音处理
## 中文名字为精准匹配 西文为匹配名或姓
def getassAuthor(request):
    data = json.loads(request.body)
    name = data.get("name")
    # print(name)
    flag = 0
    for ch in name:
        if '\u4e00' <= ch <= '\u9fa5':
            flag = 1
            break
    # if flag == 1:
    #     sytle = Style.NORMAL
    #     name = pinyin(name, sytle)
    # print(name)


    client = Elasticsearch(host_list)
    body = {}
    if flag == 1:
        body = {
            "query": {
                "match_phrase_prefix": {
                    "name": name
                }
            }
        }
    else:
        body = {
            "query": {
                "match": {
                    "name": name
                }
            }
        }

    res = client.search(index="author", filter_path=['hits.hits._source'], body=body)
    res_list = []
    if len(res) >0 :
        hits = res['hits']['hits']
        for re in hits:
            res_list.append(re['_source'])
    return JsonResponse(res_list, safe=False)


# 认领门户
def associatetoAuthor(request):
    data = json.loads(request.body)
    uid = data.get("userid")
    aid = data.get("authorid")

    user_profile = Profile.objects.get(user_id=uid)
    user_profile.is_associated = True
    user_profile.author_id = aid
    user_profile.save()

    return JsonResponse({
        "status": 0,
        "message": "associate success"
    })


# 解除认领
## 只是将is_associated字段置为False 并不将author_id字段置空
def disassociatetoAuthor(request):
    data = json.loads(request.body)
    uid = data.get("userid")

    user_profile = Profile.objects.get(user_id=uid)
    user_profile.is_associated = False
    user_profile.save()

    return JsonResponse({
        "status": 0,
        "message": "disassociate success"
    })


#门户管理 只有认领了门户的用户才能调用该功能
# 论文展示
def paperdisplay(request):
    data = json.loads(request.body)
    uid = data.get("userid")
    pid = data.get("paperid")
    user_profile = Profile.objects.get(user_id=uid)
    aid = user_profile.author_id

    client = Elasticsearch(host_list)
    body = {
        "query": {
            "term": {
                "id": aid
            }
        },
        "script": {
            "source": """
        for(int i=0;i<ctx._source.pubs.length;i++){
          if(ctx._source.pubs[i].i==params.i){
            ctx._source.pubs[i].isdisplay=params.turnto;
          }
        }
        """,
            "lang": "painless",
            "params": {
                "i": pid,
                "turnto": 1
            }
        }
    }
    client.update_by_query(index='author', body=body)

    return JsonResponse({
        "status": 0,
        "message": "change success"
    })


#论文隐藏
def papernotdisplay(request):
    data = json.loads(request.body)
    uid = data.get("userid")
    pid = data.get("paperid")
    user_profile = Profile.objects.get(user_id=uid)
    aid = user_profile.author_id

    client = Elasticsearch(host_list)
    body = {
        "query": {
            "term": {
                "id": aid
            }
        },
        "script": {
            "source": """
    for(int i=0;i<ctx._source.pubs.length;i++){
      if(ctx._source.pubs[i].i==params.i){
        ctx._source.pubs[i].isdisplay=params.turnto;
      }
    }
    """,
            "lang": "painless",
            "params": {
                "i": pid,
                "turnto": 0
            }
        }
    }
    client.update_by_query(index='author', body=body)


    return JsonResponse({
        "status": 0,
        "message": "change success"
    })

def getsimilarauthor(request):
    data = json.loads(request.body)
    aid = data.get("authorid")
    user_profile = Profile.objects.get(user_id=uid)
    aid = user_profile.author_id
    return JsonResponse(res_list, safe=False)


def getrelatedauthor(request):
    data = json.loads(request.body)
    aid = data.get("authorid")

    #获取发表的论文列表
    client = Elasticsearch(host_list)
    body = {
        "query": {
            "match": {
                "id": aid
            }
        }
    }

    res = client.search(index="author", filter_path=['hits.hits._source'], body=body)
    print(res)
    pubs = res["hits"]["hits"][0]["_source"]["pubs"]
    name = res["hits"]["hits"][0]["_source"]["name"].replace(" ","")

    res_list_temp= []
    for pub in pubs:
        body = {
            "query": {
                "match": {
                    "id": pub["i"]
                }
            }
        }
        res = client.search(index="paper", filter_path=['hits.hits._source'], body=body)
        print(res)
        if len(res)>0 :
            authors = res["hits"]["hits"][0]["_source"]["authors"]
            res_list_temp.extend(authors)
    res_list = []
    print(name)
    print()
    for re in res_list_temp:
        print(re['name'])
        count = res_list_temp.count(re)
        re["account_cooperation"] = count
        if re['name'].replace(" ","") != name:
            res_list.append(re)

    return JsonResponse(res_list, safe=False)


# 基本检索
# 作者基本检索字段：姓名 相关领域（tag） 工作单位（org）
# 论文基本检索字段：标题 刊物（venue）关键词  摘要 issn isbn doi
type = ['', 'name', 'tags', 'org',
        'title', 'venue', 'keyword', 'abstract', 'issn', 'doi']
def basicsearch(request):
    data = json.loads(request.body)
    typeid = data.get("type")
    content = data.get("content")
    orderid = data.get("order")

    client = Elasticsearch(host_list)
    body = {
        "query": {
            "match": {
                type[typeid]: content
            }
        }
    }

    if typeid <=3 :
        res = client.search(index="author", filter_path=['hits.hits._source'], body=body)
    else :
        res = client.search(index="paper", filter_path=['hits.hits._source'], body=body)

    return JsonResponse(res, safe=False)


