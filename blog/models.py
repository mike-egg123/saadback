from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
from user.models import Profile


# 博客文章数据模型
class BlogPost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100, blank=True)
    # 文章正文。保存大量文本使用 TextField
    content = models.TextField(blank=True)
    # 文章id
    blogid = models.CharField(max_length=20, blank=True)
    # 评论量
    tipnum = models.PositiveIntegerField(default=0)
    # 点赞量
    likenum = models.PositiveIntegerField(default=0)
    # 阅读量
    readnum = models.PositiveIntegerField(default=0)
    # 帖子类型
    type = models.PositiveIntegerField(default=0)
    # 是否点赞
    is_like = models.BooleanField(default=False)

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)


# 点赞
class Like(models.Model):
    liker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    liked = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    def __str__(self):
        return self.liker.user.username + " likes " + self.liked.title