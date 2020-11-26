import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from blog.models import BlogPost
from comment.models import Comment
from user.models import Profile
# Create your views here.


class CreateComment:
    @staticmethod
    def post_comment(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                blog_id = data.get('id')
                comment_body = data.get('text')
                created = timezone.now()
                blog = get_object_or_404(BlogPost, id=blog_id)
                # 尝试评论
                try:
                    # 创建新的评论对象
                    new_comment = Comment()
                    new_comment.blog = blog
                    new_comment.user = request.user
                    new_comment.body = comment_body
                    new_comment.created = created
                    # 保存后提交
                    new_comment.save()
                    # 获取用户信息
                    user_id = int(request.user.id)
                    userprofile = Profile.objects.get(user_id=user_id)
                    if userprofile.avatar and hasattr(userprofile.avatar, 'url'):
                        avatar = "http://182.92.239.145" + str(userprofile.avatar.url)
                    else:
                        avatar = ""
                    print(0)
                    return JsonResponse({
                        "error_code": 0,
                        "data": {
                          "status": 0,
                          "id": str(new_comment.id),
                          "userid": request.user.id,
                          "name": str(request.user),
                          "avatar": avatar
                        }
                    })
                except:
                    print(3)
                    return JsonResponse({
                        "status": 3,
                        "message": "评论失败！"
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
                "message": "请登录后再评论！"
            })




