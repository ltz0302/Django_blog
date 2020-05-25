from django import forms
from photologue.models import Gallery, Photo

class GalleryPostForm(forms.ModelForm):
    class Meta:
        model = Gallery
        # 定义表单包含的字段
        fields = ('title', 'slug', 'description',)


class PhotoPostForm(forms.ModelForm):
    class Meta:
        model = Photo
        # 定义表单包含的字段
        fields = ('image', 'caption',)