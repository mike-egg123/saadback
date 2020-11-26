from django.db import models
from django.contrib.auth.models import User
from blog.models import BlogPost
# Create your models here.
from user.models import Profile
from django.utils import timezone


class Comment(models.Model):
    # 被评论的文章
    blog = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
    )
    # 评论的发布者
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    # 评论id
    commentid = models.CharField(max_length=20, blank=True)
    # 评论内容
    body = models.TextField()
    # 发布时间为当前时间
    created = models.DateTimeField(default=timezone.now)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # 返回评论内容的前20个字符
        return self.body[:20]


