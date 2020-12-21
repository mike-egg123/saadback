from django.urls import path
from .views import *

urlpatterns = [
    # 发送私信
    path('sendimessage', Message.create_message),
    # 获取评论通知
    path('getcommentmessage', Message.get_comment_message),
    # 获取举报通知
    path('getreportmessage', Message.get_report_message),
    # 获取收藏通知
    path('getstarmessage', Message.get_star_message),
    # 获取私信通知
    path('getimessage', Message.get_i_message),

    # 已读评论通知
    path('readcommentmessage', Message.read_comment_message),
    # 已读举报通知
    path('readreportmessage', Message.read_report_message),
    # 已读收藏通知
    path('readstarmessage', Message.read_star_message),
    # 已读私信通知
    path('readimessage', Message.read_i_message),
]