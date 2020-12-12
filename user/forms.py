# 引入表单类
from django import forms

# 引入 User 模型
from .models import Profile


# 扩展用户信息的表单
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio', 'userid', 'birthday', 'address', 'org', 'position', 'gender', 'is_administrator', 'is_associated', 'author_id')