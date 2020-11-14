from drf_haystack.serializers import HaystackSerializer
from rest_framework.serializers import ModelSerializer

from app01 import models

from app01.search_indexes import BookIndex
class BookSerializer(ModelSerializer):
    class Meta:
        model=models.Book
        fields='__all__'
class BookIndexSerializer(HaystackSerializer):
    object = BookSerializer(read_only=True) # 只读,不可以进行反序列化

    class Meta:
        index_classes = [BookIndex]# 索引类的名称
        fields = ('text', 'object')# text 由索引类进行返回, object 由序列化类进行返回,第一个参数必须是text