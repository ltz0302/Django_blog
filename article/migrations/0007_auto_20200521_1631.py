# Generated by Django 3.0.2 on 2020-05-21 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_articlepost_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
