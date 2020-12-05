from django.urls import path
from . import views

urlpatterns = [
    path('updateacademicdb', views.update),  # 更新学术数据库
    path('associatetoAuthor', views.associatetoAuthor),  # 认领门户
]