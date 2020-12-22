from itertools import islice

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
from elasticsearch import helpers

# from elasticsearch._async import helpers

host_list = [
    '127.0.0.1:9200'
]

# 最热专家
popularAuthors = []

#最热论文
popularPapers = []


# 更新数据
## 只有两种选项可选 Paper和Author （Venue已经全部更新至数据库中）
def update(request):
    data = json.loads(request.body)
    aid = data.get("administratorid")
    # fpath = data.get("filepath")
    # filename = fpath[fpath.rfind("\\") + 1::]
    file = data.get("file")
    if file == 'paper':
        fpath = '/home/datas/aminer_papers_0.txt'
    else :
        fpath = '/home/datas/aminer_authors_0.txt'

    filename = fpath[fpath.rfind("/") + 1::]
    sline = data.get("startline")
    alines = data.get("linesnumber")
    Update_Log.objects.create(filename=filename, updateadministrator_id=aid,
                                   startlinenum=sline, finishlinenum=sline + alines)

    ufile = open(fpath, "r")
    bulks = []
    i = 0
    client = Elasticsearch(host_list)
    # Authors表需要特别处理，对其中pubs对象添加isdisplay字段

    if(file == "paper"):
        for line in islice(ufile, sline-1, sline+alines-1):
            line_json = json.loads(line)
            action = ({
                "_index": "paper",
                "_type": "_doc",
                "_source": line_json
            })
            bulks.append(action)
            i = i + 1
            if i % 100 == 0:
                i = 0

                helpers.bulk(client, bulks)
                bulks.clear()
    else :
        for line in islice(ufile, sline-1, sline+alines-1):
            line_json = json.loads(line)
            for pub in line_json['pubs']:
                pub['isdisplay'] = 1
            action = ({
                "_index": "paper",
                "_type": "_doc",
                "_source": line_json
            })
            bulks.append(action)
            i = i + 1
            if i % 100 == 0:
                i = 0

                helpers.bulk(client, bulks)
                bulks.clear()

    ufile.close()

    #获取最热专家和最热论文
    popularAuthors.clear()
    popularPapers.clear()
    body11 = {
        "query": {
            "match_all": {}
        },
        "sort": [{
            "h_index": "desc"
        }]
        , "timeout": "1s"
    }
    res = client.search(index="author", filter_path=['hits.hits._source.id', 'hits.hits._source.name',
                                                     'hits.hits._source.h_index', 'hits.hits._source.n_pubs',
                                                     'hits.hits._source.n_citation'], body=body11, size=10)

    if len(res) > 0:
        hits = res['hits']['hits']
        for re in hits:
            popularAuthors.append(re['_source'])

    body12 = {
        "query": {
            "match_all": {}
        },
        "sort": [{
            "n_citation": "desc"
        }]
        , "timeout": "1s"
    }
    res = client.search(index="paper", filter_path=['hits.hits._source.id', 'hits.hits._source.title',
                                                     'hits.hits._source.n_citation'], body=body12, size=10)

    if len(res) > 0:
        hits = res['hits']['hits']
        for re in hits:
            popularPapers.append(re['_source'])


    return JsonResponse({
        "status": 0,
        "message": "update success"
    })


# 根据文件名获取更新记录
## 下拉框可选 一共就2种 author paper
## 结果按时间排序
def getupdatebyfilename(request):
    data = json.loads(request.body)
    # aid = data.get("administratorid")
    filename = data.get("filename")
    pagenum = data.get("pagenumber")

    record = Update_Log.objects.filter(filename__icontains=filename).all().order_by("-updatetime")
    record = serialize('json', record)
    record = json.loads(record)
    record_list = []
    for re in record:
        re['fields']['updateadministrator'] = User.objects.get(id=re['fields']["updateadministrator"]).username
        record_list.append(re['fields'])
    return JsonResponse(record_list[(pagenum-1)*10: pagenum*10], safe=False)
    # return JsonResponse(record, safe=False)


# 获取可认领的门户
## 未用拼音处理
## 中文名字为精准匹配 西文为匹配名或姓
def getassAuthor(request):
    data = json.loads(request.body)
    name = data.get("name")
    pagenum = data.get("pagenumber")

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
            },
            "from": (pagenum - 1) * 10,
            "size": 10
        }

    res = client.search(index="author", filter_path=[], body=body)
    total = res['hits']['total']['value']
    res_list = []
    if len(res['hits']['hits']) > 0:
        hits = res['hits']['hits']
        for re in hits:
            res_list.append(re['_source'])
    return JsonResponse({"total": total, "res": res_list}, safe=False)


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
    aid =user_profile.author_id
    user_profile.is_associated = False
    user_profile.author_id = ""
    user_profile.save()

    # 将原本的isdisplay设置全部恢复
    client = Elasticsearch(host_list)
    body = {
        "script": {
            "source": """
                    for(int i=0;i<ctx._source.pubs.length;i++){
                        ctx._source.pubs[i].isdisplay=params.turnto;
                    }
                    """,
            "lang": "painless",
            "params": {
                "turnto": 1
            }
        },
        "query": {
            "term": {
                "id": aid
            }
        }
    }
    client.update_by_query(index='author', body=body)

    return JsonResponse({
        "status": 0,
        "message": "disassociate success"
    })


# 门户管理 只有认领了门户的用户才能调用该功能
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


# 论文隐藏
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


# 相似专家
## 准确度有待提高
def getsimilarauthor(request):
    data = json.loads(request.body)
    aid = data.get("authorid")
    pagenum = data.get("pagenumber")

    # 获取发表的论文列表
    client = Elasticsearch(host_list)
    body = {
        "query": {
            "match": {
                "id": aid
            }
        }
    }

    res = client.search(index="author", filter_path=['hits.hits._source'], body=body)
    tags = res["hits"]["hits"][0]["_source"]["tags"]

    sd = []
    for tag in tags:
        taginfo = tag["t"]
        sd.append({
            "match": {
                "tags.t": taginfo
            }
        })
    body = {
        "query": {
            "bool": {
                "should": sd
            }
        }
        ,
        "from" : (pagenum - 1)*10,
        "size" : 10
        , "sort": [
            {
                "_score": "desc"  # 排序字段，desc降序排序
            }
        ]
    }

    res = client.search(index="author", filter_path=[], body=body)
    total = res['hits']['total']['value']
    res_list = []
    if len(res['hits']['hits']) > 0:
        hits = res['hits']['hits']
        for re in hits:
            if re['_source']['id'] != aid:
                res_list.append(re['_source'])
    return JsonResponse({"total":total, "res": res_list}, safe=False)


# 相关专家
def getrelatedauthor(request):
    data = json.loads(request.body)
    aid = data.get("authorid")
    pagenum = data.get("pagenumber")

    # 获取发表的论文列表
    client = Elasticsearch(host_list)
    body = {
        "query": {
            "match": {
                "id": aid
            }
        }
    }

    res = client.search(index="author", filter_path=['hits.hits._source'], body=body)
    pubs = res["hits"]["hits"][0]["_source"]["pubs"]
    name = res["hits"]["hits"][0]["_source"]["name"].replace(" ", "")

    res_list_temp = []
    for pub in pubs:
        body = {
            "query": {
                "match": {
                    "id": pub["i"]
                }
            }
        }
        res = client.search(index="paper", filter_path=['hits.hits._source'], body=body)
        if len(res) > 0:
            authors = res["hits"]["hits"][0]["_source"]["authors"]
            res_list_temp.extend(authors)
    res_list = []
    for re in res_list_temp:
        count = res_list_temp.count(re)
        re["account_cooperation"] = count
        if re['name'].replace(" ", "") != name:
            res_list.append(re)

    return JsonResponse({"total": len(res_list), "res": res_list[(pagenum - 1)*10 : pagenum*10]}, safe=False)


# 基本检索

# 作者基本检索字段：姓名 相关领域（tag） 工作单位（org）
# 论文基本检索字段：标题 刊物（venue）关键词  摘要 issn isbn doi
# 以上10个字段 编号分别为1-10s
# 如果使用前3种检索 默认页面是作者 后6种检索 默认页面是论文
type = ['', 'name', 'tags.t', 'orgs',
        'title', 'venue.raw', 'keywords', 'abstract', 'issn', 'isbn', 'doi']

# 默认排序为综合 编号为1
# 作者排序有3种 h指数 被引用数 发表论文数 编号分别为 2 3 4
# 论文排序有2种 时间（最新） 被引用数 编号为 5 6
order = ['', '_score', 'h_index', 'n_citation', 'n_pubs',
         'year', 'n_citation']

# 字段isasc意为是否增序 1为增序 0为减序
isascend = ['desc', 'asc']


def basicsearch(request):
    data = json.loads(request.body)
    typeid = data.get("type")
    content = data.get("content")
    orderid = data.get("order")
    isasc = data.get("isasc")
    isran = data.get("isrange")
    lowran = data.get("lowrange")
    highran = data.get("highrange")
    pagenum = data.get("pagenumber")

    client = Elasticsearch(host_list)

    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            type[typeid]: content
                        }

                    }

                ]
            }
        }
        , "sort": [
            {
                order[orderid]: isascend[isasc]  # 排序字段，desc降序排序
            }
        ],
        "from": (pagenum - 1) * 10
        , "size":10
    }

    if isran == 1:
        body['query']['bool']['must'].append({
                        "range": {
                            "year": {
                                "gte": lowran,
                                "lte": highran
                            }
                        }
                    })

    if typeid <= 3:
        res = client.search(index="author", filter_path=[], body=body)
    else:
        res = client.search(index="paper", filter_path=[], body=body)


    total = res['hits']['total']['value']
    res_list = []
    if len(res['hits']['hits']) > 0:
        hits = res['hits']['hits']
        for re in hits:
            res_list.append(re['_source'])
    return JsonResponse({"total": total, "res": res_list}, safe=False)


# 高级检索，两个基本检索，用es的bool查询
# 前端多了三个参数，type1,content1,boolop
# 与基本检索相比，请求体有所变化
def multisearch(request):
    data = json.loads(request.body)
    typeid = data.get("type")
    content = data.get("content")
    typeid1 = data.get("type1")
    content1 = data.get("content1")
    boolop = data.get("boolop")
    orderid = data.get("order")
    isasc = data.get("isasc")
    isran = data.get("isrange")
    lowran = data.get("lowrange")
    highran = data.get("highrange")
    pagenum = data.get("pagenumber")

    client = Elasticsearch(host_list)

    if boolop == 'and':
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                type[typeid]: content
                            },
                            "match": {
                                type[typeid1]: content1
                            }
                        }

                    ]
                }
            },
            "sort": [
                {
                    order[orderid]: isascend[isasc]  # 排序字段，desc降序排序
                }
            ],
            "from": (pagenum - 1) * 10
            , "size":10
        }
    elif boolop == 'or':
        body = {
            "query": {
                "bool": {
                    "must": [],
                    "should": [
                        {
                            "match": {
                                type[typeid]: content
                            },
                            "match": {
                                type[typeid1]: content1
                            }
                        }

                    ]
                }
            },
            "sort": [
                {
                    order[orderid]: isascend[isasc]  # 排序字段，desc降序排序
                }
            ],
            "from": (pagenum - 1) * 10
            , "size":10
        }
    else:# if boolop == not:
        body = {
            "query": {
                "bool": {
                    "must": [],
                    "must_not": [
                        {
                            "match": {
                                type[typeid]: content
                            },
                            "match": {
                                type[typeid1]: content1
                            }
                        }

                    ]
                }
            },
            "sort": [
                {
                    order[orderid]: isascend[isasc]  # 排序字段，desc降序排序
                }
            ],
            "from": (pagenum - 1) * 10
            , "size":10
        }

    if isran == 1:
        body['query']['bool']['must'].append({
                        "range": {
                            "year": {
                                "gte": lowran,
                                "lte": highran
                            }
                        }
                    })

    if typeid <= 3:
        res = client.search(index="author", filter_path=[], body=body)
    else:
        res = client.search(index="paper", filter_path=[], body=body)


    total = res['hits']['total']['value']
    res_list = []
    if len(res['hits']['hits']) > 0:
        hits = res['hits']['hits']
        for re in hits:
            res_list.append(re['_source'])
    return JsonResponse({"total": total, "res": res_list}, safe=False)

def popularauthors(request):
    return JsonResponse(popularAuthors, safe=False)

def popularpapers(request):
    return JsonResponse(popularPapers, safe=False)


# 根据id获取论文
def getpaperbyid(request):
    data = json.loads(request.body)
    pid = data.get("paperid")

    client = Elasticsearch(host_list)
    body = {
        "query": {
            "match": {
                "id": pid
            }
        }
    }

    res = client.search(index="paper", filter_path=['hits.hits._source'], body=body)
    if len(res) > 0:
        return JsonResponse(res['hits']['hits'][0]['_source'], safe=False)
    else :
        return JsonResponse({"result": "no data in DB"})


# 根据id获取门户
def getauthorbyid(request):
    data = json.loads(request.body)
    aid = data.get("authorid")
    pagenum = data.get("pagenumber")

    client = Elasticsearch(host_list)
    body = {
        "query": {
            "match": {
                "id": aid
            }
        }
    }

    res = client.search(index="author", filter_path=['hits.hits._source'], body=body)
    if len(res) > 0:
        tatal = len(res['hits']['hits'][0]['_source']['pubs'])
        res['hits']['hits'][0]['_source']['pubs'] = res['hits']['hits'][0]['_source']['pubs'][(pagenum - 1)*10 : pagenum*10]
        return JsonResponse({"total": tatal, 'res': res['hits']['hits'][0]['_source']}, safe=False)
    else:
        return JsonResponse({"result": "no data in DB"})