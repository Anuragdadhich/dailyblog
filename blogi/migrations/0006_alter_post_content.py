# Generated by Django 5.1.7 on 2025-03-15 02:58

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogi', '0005_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
