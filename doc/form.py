from django import forms
from .models import Folder,Document

# 写文章的表单类
class FolderPostForm(forms.ModelForm):
    class Meta:
        model = Folder
        # 定义表单包含的字段
        fields = ('title',)

class DocumentPostForm(forms.ModelForm):
    class Meta:
        model = Document
        # 定义表单包含的字段
        fields = ('is_public',)