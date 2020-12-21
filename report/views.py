import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from blog.models import BlogPost
from comment.models import Comment
from message.models import Reportmessage
from report.models import Report
from user.models import Profile


# Create your views here.


class CreateReport:
    @staticmethod
    # 举报冒领门户
    def post_report_author(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                author_id = data.get('author_id')
                author_user_id = data.get('author_user_id')
                report_body = data.get('text')

                # 尝试举报
                # 创建新的举报对象
                report = Report.objects.create(user_id=request.user.id)
                report.body = report_body
                report.author_id = author_id
                report.author_user_id = author_user_id
                report.type = 1
                # 保存后提交
                report.save()

                # 生成消息通知并保存
                reportmessage = Reportmessage.objects.create(author_id=author_id,
                                                             to_user_id=author_user_id)
                # commentmessage.message = comment_body
                reportmessage.type = 1
                reportmessage.save()

                return JsonResponse({
                    "error_code": 0,
                    "data": {
                        "status": 0
                    }
                })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })

        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请登录后再举报！"
            })

    @staticmethod
    # 举报帖子
    def post_report_blog(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                blog_id = data.get('id')
                report_body = data.get('text')
                # 尝试举报
                # 创建新的举报对象
                report = Report.objects.create(user_id=request.user.id)
                report.body = report_body
                report.blog_id = blog_id
                report.type = 2
                # 保存后提交
                report.save()

                # 生成消息通知并保存
                blog = BlogPost.objects.get(id=blog_id)
                reportmessage = Reportmessage.objects.create(blog=blog.id,
                                                             to_user_id=blog.user.user.id)
                # commentmessage.message = comment_body
                reportmessage.type = 2
                reportmessage.save()

                return JsonResponse({
                    "error_code": 0,
                    "data": {
                        "status": 0
                    }
                })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })

        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请登录后再举报！"
            })

    @staticmethod
    # 举报评论
    def post_report_comment(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                comment_id = data.get('id')
                report_body = data.get('text')
                # 尝试举报
                # 创建新的举报对象
                report = Report.objects.create(user_id=request.user.id)
                report.body = report_body
                report.comment_id = comment_id
                report.type = 3
                # 保存后提交
                report.save()

                # 生成消息通知并保存
                comment = Comment.objects.get(id=comment_id)
                reportmessage = Reportmessage.objects.create(comment=comment.id,
                                                             to_user_id=comment.user.user.id)
                # commentmessage.message = comment_body
                reportmessage.type = 3
                reportmessage.save()

                return JsonResponse({
                    "error_code": 0,
                    "data": {
                        "status": 0
                    }
                })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })

        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请登录后再举报！"
            })

    @staticmethod
    # 获取冒领门户举报：举报类型type:1表示举报门户，2表示举报帖子，3表示举报评论
    def get_report_author(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                report_type = data.get('type')
                try:
                    reports = Report.objects.filter(type=report_type)
                except Exception as e:
                    return JsonResponse({
                        "status": 3,
                        "message": "没有关于冒领门户的举报！"
                    })
                else:
                    json_list = []
                    for report in reports:
                        json_dict = {}
                        user_id = report.author_user_id
                        print(user_id)
                        profile = Profile.objects.get(user_id=user_id)
                        if profile.avatar and hasattr(profile.avatar, 'url'):
                            avatar = "http://182.92.239.145" + str(profile.avatar.url)
                        else:
                            avatar = ""
                        json_dict["report_id"] = report.id
                        json_dict["author_id"] = report.author_id
                        json_dict["reason"] = report.body
                        json_dict["user_id"] = user_id
                        json_dict["user_icon"] = avatar
                        json_dict["user_name"] = profile.user.username
                        json_dict["user_name_r"] = report.user.username
                        json_dict["user_id_r"] = report.user_id
                        json_dict["time"] = report.created
                        json_list.append(json_dict)
                    return JsonResponse({
                        "error_code": 0,
                        "data": {
                            "article_reported_list": json_list
                        }
                    })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })

        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请先登录！"
            })

    @staticmethod
    # 获取帖子举报：举报类型type:1表示举报门户，2表示举报帖子，3表示举报评论
    def get_report_blog(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                report_type = data.get('type')
                reports = Report.objects.filter(type=report_type)
                json_list = []
                for report in reports:
                    json_dict = {}
                    user_id = BlogPost.objects.get(id=report.blog_id).user_id
                    profile = Profile.objects.get(user_id=user_id)
                    if profile.avatar and hasattr(profile.avatar, 'url'):
                        avatar = "http://182.92.239.145" + str(profile.avatar.url)
                    else:
                        avatar = ""
                    json_dict["report_id"] = report.id
                    json_dict["blog_id"] = report.blog_id
                    json_dict["title"] = BlogPost.objects.get(id=report.blog_id).title
                    json_dict["content"] = "<p>" + BlogPost.objects.get(id=report.blog_id).htmlcontent + "</p>"
                    json_dict["reason"] = report.body
                    json_dict["user_id"] = BlogPost.objects.get(id=report.blog_id).user_id
                    json_dict["user_icon"] = avatar
                    json_dict["user_name_r"] = profile.user.username
                    json_dict["user_id_r"] = report.user_id
                    json_dict["time"] = report.created
                    json_list.append(json_dict)
                return JsonResponse({
                    "error_code": 0,
                    "data": {
                        "article_reported_list": json_list
                    }
                })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })

        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请先登录！"
            })

    @staticmethod
    # 获取评论举报：举报类型type:1表示举报门户，2表示举报帖子，3表示举报评论
    def get_report_comment(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                report_type = data.get('type')
                reports = Report.objects.filter(type=report_type)
                json_list = []
                for report in reports:
                    json_dict = {}
                    user_id = Comment.objects.get(id=report.comment_id).user_id
                    profile = Profile.objects.get(user_id=user_id)
                    blog = BlogPost.objects.get(id=Comment.objects.get(id=report.comment_id).blog_id)
                    if profile.avatar and hasattr(profile.avatar, 'url'):
                        avatar = "http://182.92.239.145" + str(profile.avatar.url)
                    else:
                        avatar = ""
                    json_dict["report_id"] = report.id
                    json_dict["comment_id"] = report.comment_id
                    json_dict["title"] = blog.title
                    json_dict["content"] = Comment.objects.get(id=report.comment_id).body
                    json_dict["reason"] = report.body
                    json_dict["user_id"] = Comment.objects.get(id=report.comment_id).user_id
                    json_dict["user_icon"] = avatar
                    json_dict["user_name_r"] = profile.user.username
                    json_dict["user_id_r"] = report.user_id
                    json_dict["time"] = report.created
                    json_list.append(json_dict)
                return JsonResponse({
                    "error_code": 0,
                    "data": {
                        "article_reported_list": json_list
                    }
                })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })

        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请先登录！"
            })

    @staticmethod
    # 处理冒领门户举报
    def handle_report_author(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                handle_type = data.get('type')
                report_id = data.get('id')
                report = Report.objects.get(id=report_id)
                author_user_id = report.author_user_id
                author_user = Profile.objects.get(user_id=author_user_id)
                # author_user = Profile.user.objects.get(user_id=author_user_id)
                print(author_user.user.username)
                # Profile.user.objects.get(id=author_user_id)
                if handle_type == 1:
                    author_user.is_associated = False
                    author_user.author_id = 0
                    author_user.save()
                    reports = Report.objects.filter(author_id=report.author_id)
                    for a_report in reports:
                        a_report.delete()
                    return JsonResponse({
                        "data": {
                            "status": 1
                        }
                    })
                elif handle_type != 0:
                    return JsonResponse({
                        "data": {
                            "status": 0
                        }
                    })
                else:
                    report.delete()
                    return JsonResponse({
                        "data": {
                            "status": 1
                        }
                    })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })
        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请先登录！"
            })

    @staticmethod
    # 处理帖子举报
    def handle_report_blog(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                handle_type = data.get('type')
                report_id = data.get('id')
                report = Report.objects.get(id=report_id)
                blog = BlogPost.objects.get(id=report.blog_id)
                if handle_type == 1:
                    try:
                        # 删除关于该贴评论的举报
                        comments = Comment.objects.filter(blog_id=report.blog_id)
                        for comment in comments:
                            try:
                                commentreports = Report.objects.filter(comment_id=comment.id)
                            except Exception as e:
                                continue
                            else:
                                for a_commentreport in commentreports:
                                    a_commentreport.delete()
                    except Exception as e:
                        print("该贴没有评论！")
                    # 删除关于该贴的举报
                    reports = Report.objects.filter(blog_id=report.blog_id)
                    for a_report in reports:
                        a_report.delete()

                    # 删除该贴
                    blog.delete()
                    return JsonResponse({
                         "data": {
                            "status": 1
                         }
                    })
                elif handle_type != 0:
                    return JsonResponse({
                        "data": {
                            "status": 0
                        }
                    })
                else:
                    report.delete()
                    return JsonResponse({
                        "data": {
                            "status": 1
                        }
                    })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })
        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请先登录！"
            })

    @staticmethod
    # 处理评论举报
    def handle_report_comment(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                report_id = data.get('id')
                handle_type = data.get('type')
                report = Report.objects.get(id=report_id)
                comment = Comment.objects.get(id=report.comment_id)
                if handle_type == 1:
                    reports = Report.objects.filter(comment_id=report.comment_id)
                    for a_report in reports:
                        a_report.delete()
                    comment.delete()
                    return JsonResponse({
                        "data": {
                            "status": 1
                        }
                    })
                elif handle_type != 0:
                    return JsonResponse({
                        "data": {
                            "status": 0
                        }
                    })
                else:
                    report.delete()
                    return JsonResponse({
                        "data": {
                            "status": 1
                        }
                    })
            # 处理错误请求
            else:
                print(2)
                return JsonResponse({
                    "status": 2,
                    "message": "请使用post请求"
                })
        else:
            print(1)
            return JsonResponse({
                "status": 1,
                "message": "请先登录！"
            })
