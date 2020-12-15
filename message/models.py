from django.db import models
from report.models import Report
from django.contrib.auth.models import User
from blog.models import BlogPost
from comment.models import Comment

# Create your models here.


class Reportmessage(models.Model):
    # rid = models.ForeignKey(Report, on_delete=models.CASCADE) #举报id
    # message = models.CharField(max_length=500) # 消息内容
    time = models.DateTimeField(auto_now_add=True) # 时间
    to_user = models.ForeignKey(User, on_delete=models.CASCADE) # 消息接收人
    # 举报类型：1为举报门户，2为举报帖子，3为举报评论
    type = models.IntegerField(blank=True, null=True)
    # 被举报的评论（外键无法允许为空？那就只好变成id的形式了）
    comment = models.IntegerField(
        blank=True,
        null=True
    )
    # 被举报的文章
    blog = models.IntegerField(
        blank=True,
        null=True
    )
    # 被举报的门户
    author_id = models.CharField(max_length=20, blank=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-time',)

    def __str__(self):
        return 'message {}'.format(self.message)




class Commentmessage(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)  # 评论文章
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 评论用户
    time = models.DateTimeField(auto_now_add=True)  # 时间
    to_user = models.ForeignKey(User, related_name="comment_to",   on_delete=models.CASCADE)  # 消息接收人(文章发布者)
    # message = models.CharField(max_length=500)  # 消息内容

    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-time',)
    def __str__(self):
        return 'message {}'.format(self.message)
        # 内部类 class Meta 用于给 model 定义元数据



class Starmessage(models.Model):
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE) #收藏文章
    user = models.ForeignKey(User, on_delete=models.CASCADE) #评论用户
    time = models.DateTimeField(auto_now_add=True)  #时间
    to_user = models.ForeignKey(User, related_name="star_to",  on_delete=models.CASCADE) #消息接收人
    # message = models.CharField(max_length=500)  # 消息内容
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-time',)
    def __str__(self):
        return 'message {}'.format(self.message)
        # 内部类 class Meta 用于给 model 定义元数据




class Imessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 评论用户
    time = models.DateTimeField(auto_now_add=True)  # 时间
    to_user = models.ForeignKey(User, related_name="imessage_to", on_delete=models.CASCADE)  # 消息接收人
    message = models.CharField(max_length=500)  # 消息内容

    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-time',)
    def __str__(self):
        return 'message {}'.format(self.message)
        # 内部类 class Meta 用于给 model 定义元数据


