from django.db import models

# Create your models here.
class Book(models.Model):
    nid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=32)
    publish=models.CharField(max_length=32)
    price=models.DecimalField(max_digits=5,decimal_places=2)
#插入多条数据
