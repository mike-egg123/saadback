"""saadback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from blog.views import Blog
from comment.views import CreateComment
from message.views import Message
from report.views import CreateReport
from user.views import Users, Personality

from app01.views import BookSearchView

router = routers.DefaultRouter()
router.register("book/search", BookSearchView, basename="book-search")
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 用户相关接口
    path('apis/user/', include("user.urls")),
    path('apis/personality/', include("user.urls")),

    # 帖子相关接口
    path('apis/blog/', include("blog.urls")),

    # 检索门户和学术成果相关接口
    path('apis/search/', include("search.urls")),

    # 评论相关接口
    path('apis/comment/', include("comment.urls")),

    # 举报相关接口
    path("apis/report/", include("report.urls")),

    # 消息相关接口
    path("apis/message/", include("message.urls")),
]

urlpatterns += router.urls
