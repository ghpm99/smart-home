# Generated by Django 4.2.3 on 2023-08-24 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0008_videoyoutube'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VideoYoutube',
        ),
        migrations.AddField(
            model_name='video',
            name='comment_count',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='dislike_count',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='like_count',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='privacy_status',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='upload_status',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='view_count',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
