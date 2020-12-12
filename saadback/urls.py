
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from blog.views import Blog
from comment.views import CreateComment
from report.views import CreateReport
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
    path('apis/personality/change', Personality.change_personality),  # 修改用户信息
    path('apis/personality/get', Personality.get_personality),  # 得到用户信息
    path('apis/user/modifypassword', Users.modify_password),  # 修改密码
    path('apis/user/follow', Users.follow),  # 关注用户
    path('apis/user/getfolloweds', Users.getfolloweds),  # 关注用户

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
    # 举报帖子
    path('apis/blog/reportblog', CreateReport.post_report),
    # 获取用户所有评论信息
    path('apis/blog/getmycomment', Blog.getMyComment),
    # 搜索帖子
    path('apis/blog/searchblog', Blog.search_blog),

    # 返回收藏帖子列表
    path('apis/blog/collectbloglist', Blog.get_collect_blog_list),
    # 收藏或者取消收藏帖子
    path('apis/blog/setblogcollect', Blog.setBlogCollect),

    path('apis/search/', include("search.urls")),
]

#urlpatterns += router.urls
