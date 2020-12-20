from django.urls import path
from . import views

urlpatterns = [

    # 更新学术数据库
    path('updateacademicdb', views.update),

    #### 更新数据后门
    path('updateacademicdb1', views.update1),

    # 根据文件名查找更新记录
    path('getupdatebyfilename', views.getupdatebyfilename),


    # 获取可得认领门户
    path('getassAuthor', views.getassAuthor),
    # 认领门户
    path('associatetoAuthor', views.associatetoAuthor),
    # 解除门户认领
    path('disassociatetoAuthor', views.disassociatetoAuthor),

    #门户管理
    ## 论文展示
    path('paperdisplay', views.paperdisplay),
    ## 论文隐藏
    path('papernotdisplay', views.papernotdisplay),

    # 相关计算
    ##相关专家
    path('getsimilarauthor', views.getsimilarauthor),
    ##相似专家
    path('getrelatedauthor', views.getrelatedauthor),

    # 作者基本检索字段：姓名 相关领域（tag） 工作单位（org）
    # 论文基本检索字段：标题 刊物（venue）关键词  摘要 issn isbn doi
    # 以上10个字段 编号分别为1-10
    # 如果使用前3种检索 默认页面是作者 后6种检索 默认页面是论文

    # 默认排序为综合 编号为1
    # 作者排序有3种 h指数 被引用数 发表论文数 编号分别为 2 3 4
    # 论文排序有2种 时间（最新） 被引用数 编号为 5 6

    #基本检索（单字段，单关键词）
    path('basicsearch', views.basicsearch),

    # 最热专家
    path('popularauthors', views.popularauthors),

    # 最热论文
    path('popularpapers', views.popularpapers),

    #根据id获取论文
    path('getpaperbyid', views.getpaperbyid),
    #根据id获取门户
    path('getauthorbyid', views.getauthorbyid)

    #高级检索




]