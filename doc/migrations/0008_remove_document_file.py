# Generated by Django 3.0.2 on 2020-05-23 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0007_auto_20200523_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='file',
        ),
    ]
