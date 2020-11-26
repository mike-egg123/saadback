import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from blog.models import BlogPost
from comment.models import Comment
from report.models import Report
from user.models import Profile
# Create your views here.


class CreateReport:
    @staticmethod
    def post_report(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                blog_id = data.get('id')
                report_body = data.get('text')
                created = timezone.now()
                blog = get_object_or_404(BlogPost, id=blog_id)
                # 尝试举报
                try:
                    # 创建新的举报对象
                    new_report = Report()
                    new_report.blog = blog
                    new_report.user = request.user
                    new_report.body = report_body
                    new_report.created = created
                    # 保存后提交
                    new_report.save()
                    print(0)
                    return JsonResponse({
                        "error_code": 0,
                        "data": {
                          "status": 0
                        }
                    })
                except:
                    print(3)
                    return JsonResponse({
                        "status": 3,
                        "message": "举报失败！"
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




