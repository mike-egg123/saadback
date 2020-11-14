# 索引模型类的名称必须是 模型类名称 + Index
from haystack import indexes
from .models import Book
class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        """返回建立索引的模型类"""
        return Book
    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.all()
"""
说明: 
1.在BookIndex建立的字段，都可以借助haystack由elasticsearch搜索引擎查询。
2.其中text字段声明为document=True，表名该字段是主要进行关键字查询的字段， 该字段的索引值可以由多个数据库模型类字段组成(是多个字段,不是多个数据库模型类,转者注)，具体由哪些模型类字段组成，我们用use_template=True表示后续通过模板来指明。
3.在 REST framework中，索引类的字段会作为查询结果返回数据的来源, 
"""