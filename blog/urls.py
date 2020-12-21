# 引入path
from django.urls import path
from .views import *

# 正在部署的应用的名称
app_name = 'blog'

urlpatterns = [
    # 新建帖子
    path('createblog', Blog.createBlog),
    # 修改帖子
    path('editblog', Blog.editBlog),
    # 获取帖子详情
    path('getbloginfo', Blog.getBlogInfo),
    # 获取用户所有帖子信息
    path('getuserblogs', Blog.getAllBlogs),
    # 点赞/取消点赞帖子
    path('setbloglike', Blog.setBlogLike),
    # 获取用户的帖子论坛大致信息
    path('getuserbloginfo', Blog.getUserBlogInfo),
    # 获取热门帖子列表
    path('gethotblogs', Blog.getHotBlogs),
    # 获取用户5条热门帖子信息
    path('getuserhotblog', Blog.getUserHotBlog),
    # 获取用户所有评论信息
    path('getmycomment', Blog.getMyComment),
    # 搜索帖子
    path('searchblog', Blog.search_blog),
    # 返回收藏帖子列表
    path('collectbloglist', Blog.get_collect_blog_list),
    # 获取他人收藏帖子列表
    path('othercollectblog', Blog.get_other_collect_blog),
    # 收藏或者取消收藏帖子
    path('setblogcollect', Blog.setBlogCollect),
]