from django.http import JsonResponse
from django.shortcuts import render
import json

# Create your views here.
from blog.models import BlogPost
from comment.models import Comment
from message.models import Commentmessage, Reportmessage, Starmessage, Imessage
from user.models import Profile
from django.http import HttpResponse, JsonResponse


class Message:
    @staticmethod
    # 发送私信
    def create_message(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                to_user_id = data.get("id")
                message = data.get("message")
                imessage = Imessage.objects.create(user_id=request.user.id,
                                                   to_user_id=to_user_id)
                imessage.message = message
                imessage.save()
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
                "message": "请登录！"
            })

    @staticmethod
    # 获取评论通知
    def get_comment_message(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                try:
                    comment_messages = Commentmessage.objects.filter(to_user_id=request.user.id)
                    json_list = []
                    for comment_message in comment_messages:
                        try:
                            json_dict = {}
                            blog = BlogPost.objects.get(id=comment_message.blog_id)
                            profile = Profile.objects.get(user_id=comment_message.user_id)
                            json_dict["name"] = profile.user.username
                            json_dict["blog_title"] = blog.title
                            json_dict["message_id"] = comment_message.id
                            json_list.append(json_dict)
                        except Exception as e:
                            continue

                    return JsonResponse({
                        "error_code": 0,
                        "data": {
                            "msgCollection": json_list
                        }
                    })
                except Exception as e:
                    return JsonResponse({
                        "error_code": 1,
                        "data": {
                            "msgCollection": "没有评论通知"
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
                "message": "请登录！"
            })

    @staticmethod
    # 获取举报通知
    def get_report_message(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                try:
                    report_messages = Reportmessage.objects.filter(to_user_id=request.user.id)
                    json_list = []
                    for report_message in report_messages:
                        try:
                            json_dict = {"type": report_message.type}
                            if report_message.type == 2:
                                blog = BlogPost.objects.get(id=report_message.blog)
                                json_dict["message"] = blog.title
                            elif report_message.type == 3:
                                comment = Comment.objects.get(id=report_message.comment)
                                json_dict["message"] = comment.body
                            elif report_message.type == 1:
                                author_id = report_message.author_id
                                json_dict["message"] = author_id
                            json_dict["message_id"] = report_message.id
                            json_list.append(json_dict)
                        except Exception as e:
                            continue

                    return JsonResponse({
                        "error_code": 0,
                        "data": {
                            "msgCollection": json_list
                        }
                    })
                except Exception as e:
                    return JsonResponse({
                        "error_code": 1,
                        "data": {
                            "msgCollection": "没有举报通知"
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
                "message": "请登录！"
            })

    @staticmethod
    # 获取收藏通知
    def get_star_message(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                try:
                    star_messages = Starmessage.objects.filter(to_user_id=request.user.id)
                    json_list = []
                    for star_message in star_messages:
                        try:
                            json_dict = {}
                            blog = BlogPost.objects.get(id=star_message.blog.id)
                            profile = Profile.objects.get(user_id=star_message.user.id)
                            json_dict["name"] = profile.user.username
                            json_dict["blog_title"] = blog.title
                            json_dict["message_id"] = star_message.id
                            json_list.append(json_dict)
                        except Exception as e:
                            continue

                    return JsonResponse({
                        "error_code": 0,
                        "data": {
                            "msgCollection": json_list
                        }
                    })
                except Exception as e:
                    return JsonResponse({
                        "error_code": 1,
                        "data": {
                            "msgCollection": "没有收藏通知"
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
                "message": "请登录！"
            })

    @staticmethod
    # 获取私信通知
    def get_i_message(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                try:
                    imessages = Imessage.objects.filter(to_user_id=request.user.id)
                    json_list = []
                    for imessage in imessages:
                        json_dict = {}
                        print(request.user.id)
                        profile = Profile.objects.get(user_id=imessage.user.id)
                        json_dict["user"] = profile.user.username
                        json_dict["message"] = imessage.message
                        json_dict["message_id"] = imessage.id
                        json_list.append(json_dict)

                    return JsonResponse({
                        "error_code": 0,
                        "data": {
                            "msgCollection": json_list
                        }
                    })
                except Exception as e:
                    return JsonResponse({
                        "error_code": 1,
                        "data": {
                            "msgCollection": "没有私信通知"
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
                "message": "请登录！"
            })

    @staticmethod
    # 已读评论通知
    def read_comment_message(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                message_id = data.get('message_id')
                message = Commentmessage.objects.get(id=message_id)
                message.delete()
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
                "message": "请登录！"
            })

    @staticmethod
    # 已读举报通知
    def read_report_message(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                message_id = data.get('message_id')
                message = Reportmessage.objects.get(id=message_id)
                message.delete()
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
                "message": "请登录！"
            })

    @staticmethod
    # 已读收藏通知
    def read_star_message(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                message_id = data.get('message_id')
                message = Starmessage.objects.get(id=message_id)
                message.delete()
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
                "message": "请登录！"
            })

    @staticmethod
    # 已读私信通知
    def read_i_message(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                message_id = data.get('message_id')
                message = Imessage.objects.get(id=message_id)
                message.delete()
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
                "message": "请登录！"
            })
