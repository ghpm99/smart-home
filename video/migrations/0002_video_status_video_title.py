# Generated by Django 4.2.3 on 2023-08-01 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pendente'), (1, 'Processando'), (2, 'Enviando'), (2, 'Sucesso'), (3, 'Falhou')], default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]