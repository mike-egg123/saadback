from django.urls import path
from .views import *

urlpatterns = [
    # 举报冒领门户
    path('reportauthor', CreateReport.post_report_author),
    # 举报帖子
    path('reportblog', CreateReport.post_report_blog),
    # 举报评论
    path('reportcomment', CreateReport.post_report_comment),
    # 获取冒领门户举报
    path('getauthorreports', CreateReport.get_report_author),
    # 获取帖子举报
    path('getblogreports', CreateReport.get_report_blog),
    # 获取评论举报
    path('getcommentreports', CreateReport.get_report_comment),
    # 处理冒领门户举报
    path('handleauthorreport', CreateReport.handle_report_author),
    # 处理帖子举报
    path('handleblogreport', CreateReport.handle_report_blog),
    # 处理评论举报
    path('handlecommentreport', CreateReport.handle_report_comment),
]