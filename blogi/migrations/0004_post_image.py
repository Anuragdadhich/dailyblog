# Generated by Django 5.1.7 on 2025-03-14 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogi', '0003_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
