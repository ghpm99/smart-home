# Generated by Django 4.2.3 on 2023-08-25 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0009_delete_videoyoutube_video_comment_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='publish_at',
            field=models.DateTimeField(null=True),
        ),
    ]
