# Generated by Django 5.0.4 on 2024-06-11 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0004_author_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='name',
        ),
    ]
