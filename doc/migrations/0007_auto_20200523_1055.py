# Generated by Django 3.0.2 on 2020-05-23 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0006_document_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
