from django.db import models
from django.contrib.auth.models import User

from user.models import *



#更新日志模型类

class Update_Log(models.Model):
    ulid = models.AutoField(primary_key=True) #主键
    filename = models.CharField(max_length=50)  # 文件名

    startlinenum = models.PositiveIntegerField()  # 开始行数（包括本行）
    finishlinenum = models.PositiveIntegerField()  # 结束行数（不包括本行）

    updateadministrator = models.ForeignKey(User, on_delete=models.CASCADE)  # 管理员

    updatetime = models.DateTimeField(auto_now_add=True)  # 更新时间


    def __str__(self):
        return 'Update {}'.format(self.filename)