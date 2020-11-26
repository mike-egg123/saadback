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
    # 举报
    def post_report(request):
        if request.user.is_authenticated:
            # 处理 POST 请求
            if request.method == 'POST':
                data = json.loads(request.body)
                blog_id = data.get('id')
                report_body = data.get('text')
                # 尝试举报
                # 创建新的举报对象
                print(8)
                report = Report.objects.create(user_id=request.user.id, blog_id=blog_id)
                print(9)
                report.body = report_body
                # 保存后提交
                report.save()
                return JsonResponse({
                        "error_code": 0,
                        "data": {
                          "status": 0
                        }
                    })
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




