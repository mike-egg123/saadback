from django.db import models
from django.contrib.auth.models import User
from blog.models import BlogPost
from comment.models import Comment
# Create your models here.


class Report(models.Model):
    # 被举报的文章
    blog = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    # 举报人
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    # 被举报的评论（外键无法允许为空？那就只好变成id的形式了）
    comment_id = models.IntegerField(
        blank=True,
        null=True
    )
    # todo:被举报的门户
    # 举报类型：1为举报门户，2为举报帖子，3为举报评论
    type = models.IntegerField(blank=True, null=True)
    # 举报id
    reportid = models.CharField(max_length=20, blank=True)
    # 举报理由
    body = models.TextField()
    # 举报时间为当前时间
    created = models.DateTimeField(auto_now_add=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # 返回举报理由的前20个字符
        return self.body[:20]


