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
from user.views import Users, Personality

from app01.views import BookSearchView

router = routers.DefaultRouter()
router.register("book/search", BookSearchView, basename="book-search")
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('apis/user/getstatus', Users.get_status),  # 返回状态 是否登录
    path('apis/user/login', Users.login_user),  # 登录
    path('apis/user/getvalidcode', Users.get_valid_img),  # 获取验证码
    path('apis/user/logout', Users.logout_user),  # 注销
    path('apis/user/register', Users.register),  # 注册
    path('apis/personality/change', Personality.change_personality), #修改用户信息
    path('apis/personality/get', Personality.get_personality), # 得到用户信息

    path('apis/search/', include('search.urls')),  # 学术数据库相关
]

#urlpatterns += router.urls
