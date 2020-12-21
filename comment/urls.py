from django.urls import path
from .views import *

urlpatterns = [
    # 创建评论
    path('create', CreateComment.post_comment),
]