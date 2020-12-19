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
    path('apis/user/getstatus', Users.get_status),  # 获取登录状态
    path('apis/user/login', Users.login_user),  # 登录
    path('apis/user/getvalidcode', Users.get_valid_img),  # 获取验证码
    path('apis/user/logout', Users.logout_user),  # 注销
    path('apis/user/register', Users.register),  # 注册
    path('apis/personality/change', Personality.change_personality),  # 修改用户信息
    path('apis/personality/get', Personality.get_personality),  # 得到用户信息
    path('apis/user/modifypassword', Users.modify_password),  # 修改密码
    path('apis/user/change_follow_state', Users.follow),  # 切换关注状态
    path('apis/user/getfolloweds', Users.getfolloweds),  # 获取当前用户关注的所有用户
    path('apis/user/get_follow_state', Users.get_follow_state),  # 请求关注状态，即当前用户是否关注了目标用户
    path('apis/user/get_userid_by_authorid', Users.get_userid_by_authorid),  # 根据门户id寻找用户id

    # 新建帖子
    path('apis/blog/createblog', Blog.createBlog),
    # 修改帖子
    path('apis/blog/editblog', Blog.editBlog),
    # 获取帖子详情
    path('apis/blog/getbloginfo', Blog.getBlogInfo),
    # 获取用户所有帖子信息
    path('apis/blog/getuserblogs', Blog.getAllBlogs),
    # 点赞/取消点赞帖子
    path('apis/blog/setbloglike', Blog.setBlogLike),
    # 获取用户的帖子论坛大致信息
    path('apis/blog/getuserbloginfo', Blog.getUserBlogInfo),
    # 获取热门帖子列表
    path('apis/blog/gethotblogs', Blog.getHotBlogs),
    # 获取用户5条热门帖子信息
    path('apis/blog/getuserhotblog', Blog.getUserHotBlog),
    # 评论
    path('apis/blog/comment', CreateComment.post_comment),
    # 获取用户所有评论信息
    path('apis/blog/getmycomment', Blog.getMyComment),
    # 搜索帖子
    path('apis/blog/searchblog', Blog.search_blog),

    # 返回收藏帖子列表
    path('apis/blog/collectbloglist', Blog.get_collect_blog_list),
    # 获取他人收藏帖子列表
    path('apis/blog/othercollectblog', Blog.get_other_collect_blog),
    # 收藏或者取消收藏帖子
    path('apis/blog/setblogcollect', Blog.setBlogCollect),

    path('apis/search/', include("search.urls")),

    # 举报冒领门户
    path('apis/blog/reportauthor', CreateReport.post_report_author),
    # 举报帖子
    path('apis/blog/reportblog', CreateReport.post_report_blog),
    # 举报评论
    path('apis/blog/reportcomment', CreateReport.post_report_comment),
    # 获取冒领门户举报
    path('apis/report/getauthorreports', CreateReport.get_report_author),
    # 获取帖子举报
    path('apis/report/getblogreports', CreateReport.get_report_blog),
    # 获取评论举报
    path('apis/report/getcommentreports', CreateReport.get_report_comment),
    # 处理冒领门户举报
    path('apis/report/handleauthorreport', CreateReport.handle_report_author),
    # 处理帖子举报
    path('apis/report/handleblogreport', CreateReport.handle_report_blog),
    # 处理评论举报
    path('apis/report/handlecommentreport', CreateReport.handle_report_comment),

    # 发送私信
    path('apis/message/sendmeaasge', Message.create_message),
    # 获取评论通知
    path('apis/message/getcommentmessage', Message.get_comment_message),
    # 获取举报通知
    path('apis/message/getreportmessage', Message.get_report_message),
    # 获取收藏通知
    path('apis/message/getstarmessage', Message.get_star_message),
    # 获取私信通知
    path('apis/message/getimessage', Message.get_i_message),

    # 已读评论通知
    path('apis/message/readcommentmessage', Message.read_comment_message),
    # 已读举报通知
    path('apis/message/readreportmessage', Message.read_report_message),
    # 已读收藏通知
    path('apis/message/readstarmessage', Message.read_star_message),
    # 已读私信通知
    path('apis/message/readimessage', Message.read_i_message),

]

urlpatterns += router.urls
