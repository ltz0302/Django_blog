from django.db import models
from django.utils import timezone
# Create your models here.


class Folder(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    def __str__(self):
        return self.title

class Document(models.Model):
    title = models.CharField(max_length=100)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)
    def __str__(self):
        return self.title