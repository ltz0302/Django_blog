from django.db import models

# Create your models here.


class Folder(models.Model):
    title = models.CharField(max_length=100)


class Document(models.Model):
    title = models.CharField(max_length=100)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)