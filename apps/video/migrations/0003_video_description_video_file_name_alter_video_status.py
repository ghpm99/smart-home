# Generated by Django 4.2.3 on 2023-08-02 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_video_status_video_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='file_name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pendente'), (1, 'Processando'), (2, 'Processamento falhou'), (3, 'Processamento concluido'), (4, 'Enviando'), (6, 'Sucesso'), (7, 'Falhou')], default=0),
        ),
    ]
