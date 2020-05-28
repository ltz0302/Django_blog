from django import forms
from .models import DiaryPost

# 写文章的表单类
class DiaryPostForm(forms.ModelForm):
    class Meta:
        model = DiaryPost
        # 定义表单包含的字段
        fields = ('title', 'body', 'created',)