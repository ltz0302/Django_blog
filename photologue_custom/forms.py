from django import forms
from photologue.models import Gallery

class GalleryPostForm(forms.ModelForm):
    class Meta:
        model = Gallery
        # 定义表单包含的字段
        fields = ('title', 'slug', 'description', 'is_public',)