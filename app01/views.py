from django.shortcuts import render

# Create your views here.
from drf_haystack.viewsets import HaystackViewSet
from app01.models import Book
from app01.serializers import BookIndexSerializer
class BookSearchView(HaystackViewSet):
    index_models = [Book]

    serializer_class = BookIndexSerializer
#该视图会返回搜索结果的列表数据，所以如果可以为视图增加REST framework的分页功能。
#我们在配置文件已经定义了分页配置，所以此搜索视图会进行分页
