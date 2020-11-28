# 引入redirect重定向模块
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse, JsonResponse
# 引入刚才定义的ArticlePostForm表单类
from comment.models import Comment
from user.models import Profile
from .forms import BlogPostForm
# 引入User模型
from django.contrib.auth.models import User
import json

from .models import BlogPost, Like


class Blog:
    @staticmethod
    # 创建帖子
    def createBlog(request):
        # 判断用户是否提交数据
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "status": 2,
                    "massage": "请先登录"
                })
            data = json.loads(request.body)
            type = data.get("type")
            blog = BlogPost.objects.create(user_id=request.user.id)
            blog.type = type
            blog.save()
            # 完成后返回到文章列表
            return JsonResponse({
                "status": 0,
                "message": "创建帖子成功",
                "blogid": blog.id
            })
        # 如果用户请求获取数据
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 修改帖子
    def editBlog(request):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "status": 4,
                    "massage": "请先登录"
                })
            data = json.loads(request.body)
            blogid = data.get("id")
            title = data.get("name")
            content = data.get("content")
            type = data.get("type")
            if blogid is not None and type is not None:
                try:
                    blog = BlogPost.objects.get(id=blogid)
                    blog.title = title
                    blog.content = content
                    blog.type = type
                    blog.save()
                    return JsonResponse({
                        "status": 0,
                        "message": "帖子修改成功！"
                    })
                except:
                    return JsonResponse({
                        "status": 2,
                        "message": "帖子修改失败"
                    })
            else:
                return JsonResponse({
                    "status": 3,
                    "message": "blogid或type必填！"
                })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 获取帖子详情
    def getBlogInfo(request):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "status": 3,
                    "massage": "请先登录"
                })
            data = json.loads(request.body)
            blogid = data.get("id")
            print(blogid)
            print(0)
            if blogid is not None:
                blog = BlogPost.objects.get(id=blogid)
                blog.readnum = blog.readnum + 1
                blog.save(update_fields=['readnum'])
                comments = Comment.objects.filter(blog=blogid)
                print(9)
                print(blogid)
                json_tiplist = []
                print(2)
                for comment in comments:
                    # 获取用户信息
                    user_id = int(comment.user.id)
                    userprofile = Profile.objects.get(user_id=user_id)
                    if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                        avatar = "http://182.92.239.145" + str(userprofile.avatar.url)
                    else:
                        avatar = ""

                    json_dict = {}
                    json_dict["id"] = user_id
                    json_dict["name"] = userprofile.user.username
                    json_dict["img"] = avatar
                    json_dict["content"] = comment.body
                    json_tiplist.append(json_dict)
                return JsonResponse({
                            "status": 0,
                            "message": "帖子详情查看成功！",
                            "data": {
                                "title": str(blog.title),
                                "blogContent": str(blog.content),
                                "type": blog.type,
                                "date": blog.created,
                                "readnum": blog.readnum,
                                "tipnum": blog.tipnum,
                                "likenum": blog.likenum,
                                "like": blog.is_like,
                                "tiplist": json_tiplist
                            }
                        })

            else:
                return JsonResponse({
                    "status": 2,
                    "message": "查看帖子失败"
                })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 获取用户所有帖子信息
    def getAllBlogs(request):
        if request.method == "POST":
            data = json.loads(request.body)
            userid = data.get('id')
            blogs = BlogPost.objects.filter(user_id=userid)
            json_list = []
            for blog in blogs:
                json_dict = {}
                json_dict["blogid"] = blog.id
                json_dict["title"] = blog.title
                json_dict["content"] = blog.content
                json_dict["date"] = blog.created
                json_dict["readnum"] = blog.readnum
                json_dict["likenum"] = blog.likenum
                json_dict["tipnum"] = blog.tipnum
                json_list.append(json_dict)
            return JsonResponse({
                "status": 0,
                "data":{
                    "list":json_list
                }
            }, safe=False)
        else:
            return JsonResponse({
                "status":1,
                "message":"error method"
            })

    @staticmethod
    # 点赞/取消点赞
    def setBlogLike(request):
        if request.method == "POST":
            data = json.loads(request.body)
            blogid = data.get("id")
            like = data.get("type") # 0 点赞，1 取消点赞
            blog = BlogPost.objects.get(id=blogid)
            if not blog:
                return JsonResponse({
                    "status": 2,
                    "message": "不存在该作者或者该帖子"
                })
            if like == 1:
                likes = Like.objects.filter(liker_id=request.user.id, liked_id=blogid)
                for like in likes:
                    like.delete()
                    blog.likenum = blog.likenum - 1
                    blog.save()
                return JsonResponse({
                    "status": 0,
                    "message": "dislike success"
                })
            else:
                if Like.objects.filter(liker_id=request.user.id, liked_id=blogid):
                    return JsonResponse({
                        "status": 2,
                        "isrepeat": "already like"
                    })
                else:
                    like = Like.objects.create(liker_id=request.user.id, liked_id=blogid)
                    like.save()
                    blog.likenum = blog.likenum + 1
                    blog.save()
                    return JsonResponse({
                        "status": 0,
                        "message": str(like),
                    })
        else:
            return JsonResponse({
                "status":1,
                "message":"error method"
            })

    @staticmethod
    # 获取用户的帖子论坛大致信息
    def getUserBlogInfo(requset):
        if requset.method == "POST":
            data = json.loads(requset.body)
            userid = data.get("id")
            user = User.objects.get(id=userid)
            profile = Profile.objects.get(user_id=userid)
            blogs = BlogPost.objects.filter(user_id=userid)
            blogNum = 0
            likeNum = 0
            tipNum = 0
            avatar = "http://182.92.239.145" + str(profile.avatar.url)

            if user:
                for blog in blogs:
                    likeNum = likeNum + blog.likenum
                    tipNum = tipNum + blog.tipnum
                    blogNum = blogNum + 1
                return JsonResponse({
                    "avatar": avatar,
                    "username": str(user.username),
                    "blogNum": blogNum,
                    "likeNum": likeNum,
                    "tipNum": tipNum
                })
            else:
                return JsonResponse({
                    "status": 2,
                    "message": "该用户不存在"
                })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    # 获取热门帖子信息列表
    def getHotBlogs(request):
        if request.method == "POST":
            data = json.loads(request.body)
            type = data.get("type")
            print(type)
            blogs = BlogPost.objects.filter(type=type).order_by("-readnum")
            print(blogs)
            json_list = []
            for blog in blogs:
                json_dict = {}
                profile = Profile.objects.get(user_id=blog.user_id)
                if profile.avatar and hasattr(profile.avatar, 'url'):
                    avatar = "http://182.92.239.145" + str(profile.avatar.url)
                else:
                    avatar = ""
                json_dict['blogname'] = blog.title
                json_dict['avatar'] = avatar
                json_dict['readnum'] = blog.readnum
                json_dict['likenum'] = blog.likenum
                json_dict['tipnum'] = blog.tipnum
                json_dict['userid'] = blog.user_id
                json_dict['content'] = blog.content
                json_list.append(json_dict)
            return JsonResponse({
                "status": 0,
                "data": {
                    "list": json_list
                }
            }, safe=False)
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })

    @staticmethod
    def getUserHotBlog(request):
        if request.method == "POST":
            data = json.loads(request.body)
            userid = data.get('id')
            user = User.objects.get(id=userid)
            print(user)
            if user:
                print(userid)
                blogs = BlogPost.objects.filter(user_id=userid).order_by('-readnum')
                json_list = []
                i = 0
                for blog in blogs:
                    json_dict = {}
                    json_dict['blogname'] = blog.title
                    json_dict['blogid'] = blog.id
                    json_dict['readnum'] = blog.readnum
                    json_list.append(json_dict)
                    i = i + 1
                    if i >= 5:
                        break
                return JsonResponse({
                    "status": 0,
                    "data": {
                        "list": json_list
                    }
                }, safe=False)
            else:
                return JsonResponse({
                "status": 2,
                "message": "不存在该用户"
            })
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })


    @staticmethod
    # 获取用户所有评论信息
    def getMyComment(request):
        if request.method == "POST":
            if not request.user.is_authenticated:
                return JsonResponse({
                    "massage": "请先登录"
                })
            userid = request.user.id
            comments = Comment.objects.filter(user=userid)
            json_list = []
            for comment in comments:
                json_dict = {}
                blog = comment.blog
                profile = Profile.objects.get(user_id=blog.user_id)
                if profile.avatar and hasattr(profile.avatar, 'url'):
                    avatar = "http://182.92.239.145" + str(profile.avatar.url)
                else:
                    avatar = ""
                user = User.objects.get(id=blog.user_id)
                json_dict['date'] = comment.created
                json_dict['blogid'] = blog.id
                json_dict['blogname'] = blog.title
                json_dict['content'] = comment.body
                json_dict['img'] = avatar
                json_dict['username'] = user.username
                json_dict['userid'] = blog.user_id
                json_dict['readnum'] = blog.readnum
                json_dict['likenum'] = blog.likenum
                json_dict['tipnum'] = blog.tipnum
                json_list.append(json_dict)
            return JsonResponse({
                "status": 0,
                "data": {
                    "list": json_list
                }
            }, safe=False)
        else:
            return JsonResponse({
                "status": 1,
                "message": "error method"
            })


