# Generated by Django 5.1.7 on 2025-03-14 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
