# Generated by Django 5.0 on 2024-01-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='activte',
        ),
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]