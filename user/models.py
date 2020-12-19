from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    # 与User模型形成一对一的映射关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    avatar = models.ImageField(upload_to="avatar/%Y%m%d/", blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)
    # 用户id
    userid = models.CharField(max_length=20, blank=True)
    # 生日
    birthday = models.CharField(max_length=100, blank=True)
    # 地址
    address = models.CharField(max_length=20, blank=True)
    # 工作单位
    org = models.CharField(max_length=40, blank=True)
    # 职务
    position = models.CharField(max_length=20, blank=True)
    # 性别
    gender = models.CharField(max_length=20, blank=True)
    # 是否为管理员
    is_administrator = models.BooleanField(default=False)
    # 是否认领了门户
    is_associated = models.BooleanField(default=False)
    # 门户id（todo:暂时做成这种id的形式，后面有了门户列表可以用外键关联）
    author_id = models.CharField(max_length=1000, blank=True)
    # 真实姓名
    realname = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    followed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed'
    )

    def __str__(self):
        return '{} has followed {}'.format(self.follower.username, self.followed.username)
